import asyncio
import uvicorn
from fastapi.staticfiles import StaticFiles
from main import app
from websocket_client import connect_websocket
from database import Database

# Mount static files (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

async def start_websocket_client():
    await Database.connect_db()
    await connect_websocket()

@app.on_event("startup")
async def startup_event():
    # Start WebSocket client in background
    asyncio.create_task(start_websocket_client())

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)