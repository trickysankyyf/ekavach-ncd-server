from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

USER_ID = "new_p_puran"
PASSWORD = "Sanky@2000"


class LoginRequest(BaseModel):
    user_id: str
    password: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/api/status")
def status():
    return {
        "status": "ok",
        "message": "Server connected"
    }


@app.post("/api/login")
def login(data: LoginRequest):
    if data.user_id == USER_ID and data.password == PASSWORD:
        return {
            "status": "ok",
            "message": "Login successful"
        }

    return {
        "status": "error",
        "message": "Invalid user ID or password"
    }
