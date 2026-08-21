from workers import WorkerEntrypoint
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import asgi
import secrets

app = FastAPI()


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
        "message": "Server connected"
    }


# =========================
# LOGIN
# =========================

@app.post("/{path:path}")
async def login_catch_all(path: str, request: Request):

    token = secrets.token_urlsafe(32)

    print("LOGIN:", path)

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "token": token,
            "message": "Login successful"
        }
    )


# =========================
# WEBSOCKET RELAY
# =========================

@app.websocket("/ws/relay")
async def relay(websocket: WebSocket):

    token = websocket.query_params.get("token")

    print("WS CONNECT REQUEST")
    print("TOKEN:", bool(token))

    if not token:
        await websocket.close(code=1008)
        print("WS CLOSED: token missing")
        return

    await websocket.accept()

    print("WS CONNECTED")

    try:

        while True:

            message = await websocket.receive_text()

            print("RPC FROM APP:")
            print(message)

            # IMPORTANT:
            # Abhi received RPC ko echo nahi karna,
            # warna RPC loop ban jayega.

    except WebSocketDisconnect:

        print("WS DISCONNECTED")

    except Exception as e:

        print("WS ERROR:", str(e))


# =========================
# WORKER ENTRYPOINT
# =========================

class Default(WorkerEntrypoint):

    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)