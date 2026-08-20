from workers import WorkerEntrypoint
from fastapi import FastAPI
import asgi

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "message": "Server connected"}

@app.get("/api/status")
async def status():
    return {"status": "ok", "message": "Server connected"}

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)
