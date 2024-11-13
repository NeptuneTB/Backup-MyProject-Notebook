from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from datetime import datetime
import asyncio
import websockets
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import threading
import logging

# โหลดตัวแปรสภาพแวดล้อม
load_dotenv()

# การตั้งค่า Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")  # กำหนดค่าคีย์ลับ

# การตั้งค่า SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# การเชื่อมต่อ MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['machine_db']
collection = db['machine_data']

# ตั้งค่าการบันทึก log
logging.basicConfig(
    filename='machine_data.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# WebSocket client เพื่อรับข้อมูลจากเครื่องจักร
async def websocket_client():
    uri = "ws://technest.ddns.net:8001/ws"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                async for message in websocket:
                    parsed_data = json.loads(message)
                    parsed_data['timestamp'] = datetime.utcnow()
                    
                    collection.insert_one(parsed_data)
                    
                    socketio.emit('machine_data', parsed_data)
        except (websockets.exceptions.ConnectionClosedError, Exception) as e:
            logging.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # รอ 5 วินาทีก่อนลองเชื่อมต่อใหม่

# ฟังก์ชันเริ่ม WebSocket ใน thread แยก
def start_websocket_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_client())

websocket_thread = None

@app.route('/start-websocket', methods=['GET'])
def start_ws():
    global websocket_thread
    if websocket_thread is None or not websocket_thread.is_alive():
        websocket_thread = threading.Thread(target=start_websocket_client, daemon=True)
        websocket_thread.start()
        return jsonify({"message": "WebSocket client started"}), 200
    return jsonify({"message": "WebSocket client already running"}), 200

@app.route('/ws-status', methods=['GET'])
def websocket_status():
    status = "running" if websocket_thread and websocket_thread.is_alive() else "stopped"
    return jsonify({"status": status}), 200

@app.route('/routes', methods=['GET'])
def api_routes():
    routes = {
        "/": "HTML หน้าแรก",
        "/start-websocket": "เริ่มต้น WebSocket Client",
        "/ws-status": "ตรวจสอบสถานะ WebSocket",
        "/api/machine-data (GET)": "ดึงข้อมูล machine data",
        "/api/machine-data (POST)": "เพิ่มข้อมูล machine data",
        "/api/machine-data/<data_id> (PUT)": "แก้ไขข้อมูล machine data",
        "/api/machine-data/<data_id> (DELETE)": "ลบข้อมูล machine data"
    }
    return jsonify(routes)

# CRUD API
@app.route('/api/machine-data', methods=['GET'])
def get_machine_data():
    limit = int(request.args.get('limit', 100))
    data = list(collection.find({}, {'_id': 1, 'timestamp': 1, 'value': 1}).sort('timestamp', -1).limit(limit))
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data), 200

@app.route('/api/machine-data', methods=['POST'])
def add_machine_data():
    data = request.json
    data['timestamp'] = datetime.utcnow()
    collection.insert_one(data)
    logging.info(f"New machine data added: {data}")
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/api/machine-data/<string:data_id>', methods=['PUT'])
def update_machine_data(data_id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(data_id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({"message": "Data updated successfully"}), 200
    return jsonify({"message": "Data not found"}), 404

@app.route('/api/machine-data/<string:data_id>', methods=['DELETE'])
def delete_machine_data(data_id):
    result = collection.delete_one({'_id': ObjectId(data_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Data deleted successfully"}), 200
    return jsonify({"message": "Data not found"}), 404

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Machine Data Monitor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .chart-container { margin-top: 20px; }
        #messages { height: 200px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <button onclick="startWebSocket()">Start WebSocket Connection</button>
        <div class="chart-container">
            <canvas id="machineChart"></canvas>
        </div>
        <div id="messages"></div>
    </div>
    <script>
        let chart;
        function startWebSocket() {
            fetch('/start-websocket').then(res => res.json()).then(data => {
                console.log(data.message);
                initializeWebSocket();
            });
        }
        function initializeWebSocket() {
            const socket = io();
            socket.on('machine_data', function(data) {
                document.getElementById('messages').innerHTML += `<div>${JSON.stringify(data)}</div>`;
                updateChart(data.value);
            });
        }
        function updateChart(value) {
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
            }
            chart.data.labels.push(new Date().toLocaleTimeString());
            chart.data.datasets[0].data.push(value);
            chart.update();
        }
        function initializeChart() {
            const ctx = document.getElementById('machineChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{ label: 'Machine Data', data: [], borderColor: 'rgb(75, 192, 192)', tension: 0.1 }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        }
        initializeChart();
    </script>
</body>
</html>
    """

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
