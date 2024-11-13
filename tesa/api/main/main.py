from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
import asyncio
import uvicorn

from models import MachineData, Token, User
from database import Database
from auth import create_access_token, get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await Database.connect_db()
    # Start WebSocket client in background
    asyncio.create_task(connect_websocket())

@app.on_event("shutdown")
async def shutdown_event():
    await Database.close_db()

# Authentication endpoints
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users_collection = await Database.get_users_collection()
    user = await users_collection.find_one({"username": form_data.username})
    
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Machine data endpoints
@app.post("/machine-data")
async def create_machine_data(data: MachineData, current_user: str = Depends(get_current_user)):
    collection = await Database.get_collection()
    await collection.insert_one(data.dict())
    return {"status": "success"}

@app.get("/machine-data")
async def get_machine_data(current_user: str = Depends(get_current_user)):
    collection = await Database.get_collection()
    data = await collection.find().sort("timestamp", -1).limit(100).to_list(None)
    return data

@app.put("/machine-data/{data_id}")
async def update_machine_data(data_id: str, data: MachineData, current_user: str = Depends(get_current_user)):
    collection = await Database.get_collection()
    await collection.update_one({"_id": data_id}, {"$set": data.dict()})
    return {"status": "success"}

@app.delete("/machine-data/{data_id}")
async def delete_machine_data(data_id: str, current_user: str = Depends(get_current_user)):
    collection = await Database.get_collection()
    await collection.delete_one({"_id": data_id})
    return {"status": "success"}

# WebSocket endpoint for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    collection = await Database.get_collection()
    
    try:
        while True:
            # Get latest data
            latest_data = await collection.find().sort("timestamp", -1).limit(1).to_list(None)
            if latest_data:
                await websocket.send_json(latest_data[0])
            await asyncio.sleep(1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)