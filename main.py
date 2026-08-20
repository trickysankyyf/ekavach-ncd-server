from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/status")
def status():
    return {
        "status": "ok",
        "message": "Server connected"
    }
