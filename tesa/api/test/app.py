import asyncio
import websockets
import json
from database import insert_machine_data
from flask import Flask, render_template
from api import app

async def receive_data():
    async with websockets.connect("ws://technest.ddns.net:8001/ws") as websocket:
        while True:
            data = await websocket.recv()
            data_json = json.loads(data)
            insert_machine_data(data_json)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # ใช้ asyncio.run() สำหรับ event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(receive_data())
    
    # เรียก Flask App ใน thread อื่น
    from threading import Thread
    def run_flask():
        app.run(debug=True, use_reloader=False)
    
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # รัน event loop หลัก
    loop.run_forever()
