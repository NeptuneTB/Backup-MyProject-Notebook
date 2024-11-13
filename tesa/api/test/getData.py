import asyncio
import websockets
import pymongo
from datetime import datetime

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["machine_db"]
collection = db["machine_data"]

# WebSocket client
async def receive_machine_data(api_key):
    async with websockets.connect("ws://technest.ddns.net:8001/ws") as websocket:
        await websocket.send(api_key)
        async for message in websocket:
            data = eval(message)  # Assuming the data is sent as a string representation of a dictionary
            data["timestamp"] = datetime.now()
            collection.insert_one(data)

def main():
    api_key = "670a935a14221a12ae886117c99cacc7"
    asyncio.get_event_loop().run_until_complete(receive_machine_data(api_key))

if __name__ == "__main__":
    main()