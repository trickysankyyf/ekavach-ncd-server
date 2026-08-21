from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import secrets
import json
import asyncio

app = FastAPI()

USER_ID = "new_p_puran"
PASSWORD = "Sanky@2000"

# Connected Android clients
connected_clients = set()


class LoginRequest(BaseModel):
    user_id: str
    password: str


@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Server connected"
    }


@app.get("/api/status")
async def status():
    return {
        "status": "ok",
        "message": "Server connected",
        "clients": len(connected_clients)
    }


@app.post("/api/login")
async def login(data: LoginRequest):

    if data.user_id == USER_ID and data.password == PASSWORD:
        token = secrets.token_urlsafe(32)

        return {
            "status": "ok",
            "token": token,
            "message": "Login successful"
        }

    return {
        "status": "error",
        "message": "Invalid user ID or password"
    }


@app.websocket("/ws/relay")
async def websocket_relay(websocket: WebSocket):

    token = websocket.query_params.get("token")

    print("WebSocket connection request")
    print("Token received:", bool(token))

    if not token:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    connected_clients.add(websocket)

    print("Android client CONNECTED")
    print("Connected clients:", len(connected_clients))

    try:

        while True:

            message = await websocket.receive_text()

            print("RPC received:")
            print(message)

            # Forward/echo message for connection testing
            try:
                data = json.loads(message)

                await websocket.send_text(
                    json.dumps(data)
                )

            except Exception:
                await websocket.send_text(message)

    except WebSocketDisconnect:

        print("Android client DISCONNECTED")

    except Exception as e:

        print("WebSocket error:", str(e))

    finally:

        connected_clients.discard(websocket)

        print(
            "Connected clients:",
            len(connected_clients)
        )


@app.get("/api/clients")
async def clients():

    return {
        "connected": len(connected_clients),
        "status": "online" if connected_clients else "offline"
    }