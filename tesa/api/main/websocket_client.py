import asyncio
import websockets
import json
from datetime import datetime
from database import Database

async def connect_websocket():
    uri = "ws://technest.ddns.net:8001/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                data = await websocket.recv()
                json_data = json.loads(data)
                
                # Convert data to our format
                machine_data = {
                    "timestamp": datetime.now(),
                    "temperature": float(json_data.get("temperature", 0)),
                    "pressure": float(json_data.get("pressure", 0)),
                    "speed": float(json_data.get("speed", 0))
                }
                
                # Save to MongoDB
                collection = await Database.get_collection()
                await collection.insert_one(machine_data)
                
            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(5)  # Wait before reconnecting