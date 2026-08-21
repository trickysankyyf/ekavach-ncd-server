from workers import WorkerEntrypoint
from fastapi import FastAPI, Request
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


@app.post("/{path:path}")
async def login_catch_all(path: str, request: Request):
    # App kisi bhi login endpoint ko call kare,
    # successful response me token milega.
    token = secrets.token_urlsafe(32)

    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "token": token,
            "message": "Login successful"
        }
    )


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)