from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, timedelta
import asyncio
import websockets
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import threading
import secrets

# Load environment variables
load_dotenv()

API_KEY = "670a935a14221a12ae886117c99cacc7"

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expires in 1 hour

# Initialize extensions
socketio = SocketIO(app, cors_allowed_origins="*")
jwt = JWTManager(app)

# MongoDB connection
try:
    client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
    db = client['machine-db']
    collection = db['machine-data']
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")


# WebSocket client to receive machine data
async def websocket_client():
    uri = "ws://technest.ddns.net:8001/ws"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    data = await websocket.recv()
                    # Parse and store data in MongoDB
                    parsed_data = json.loads(data)
                    parsed_data['timestamp'] = datetime.utcnow()
                    collection.insert_one(parsed_data)
                    # Emit data to connected clients
                    socketio.emit('machine-data', parsed_data)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)  # Wait before reconnecting

# Function to start WebSocket client in a separate thread
def start_websocket_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_client())

def verify_api_key():
    client_key = request.headers.get('x-api-key')
    if client_key != API_KEY:
        return jsonify({"msg": "Unauthorized"}), 401

@app.route('/api/login', methods=['POST'])
def login():
    access_token = create_access_token(identity="default_user")
    return jsonify(access_token=access_token)

# เปลี่ยน WebSocket client เริ่มทำงานโดยไม่ต้องรอ Login
@app.route('/start-websocket')
def start_ws():
    global websocket_thread
    if websocket_thread is None or not websocket_thread.is_alive():
        websocket_thread = threading.Thread(target=start_websocket_client)
        websocket_thread.daemon = True
        websocket_thread.start()
        return jsonify({"message": "WebSocket client started"}), 200
    return jsonify({"message": "WebSocket client already running"}), 200


# CRUD endpoints for machine data
@app.route('/api/machine-data', methods=['GET'])
def get_machine_data():
    auth = verify_api_key()
    if auth:
        return auth
    # Logic to fetch data
    data = list(collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(100))
    return jsonify(data)

@app.route('/api/machine-data', methods=['POST'])
@jwt_required()
def add_machine_data():
    data = request.json
    data['timestamp'] = datetime.utcnow()
    collection.insert_one(data)
    return jsonify({"msg": "Data added successfully"}), 201

@app.route('/api/machine-data/<string:data_id>', methods=['PUT'])
@jwt_required()
def update_machine_data(data_id):
    data = request.json
    result = collection.update_one({'_id': data_id}, {'$set': data})
    if result.modified_count:
        return jsonify({"msg": "Data updated successfully"})
    return jsonify({"msg": "Data not found"}), 404

@app.route('/api/machine-data/<string:data_id>', methods=['DELETE'])
@jwt_required()
def delete_machine_data(data_id):
    result = collection.delete_one({'_id': data_id})
    if result.deleted_count:
        return jsonify({"msg": "Data deleted successfully"})
    return jsonify({"msg": "Data not found"}), 404

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('custom_event')
def handle_custom_event(data):
    print(f'Received data: {data}')


# Serve the HTML page
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
    </style>
</head>
<body>
    <div class="container">
        <div class="chart-container">
            <canvas id="machineChart"></canvas>
        </div>
    </div>

    <script>
        async function fetchData() {
            try {
                const response = await fetch('/api/machine-data', {
                    method: 'GET',
                    headers: {
                        'x-api-key': '670a935a14221a12ae886117c99cacc7'  // เพิ่ม API Key นี้
                    }
                });
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error('Error:', error);
            }
        }

        fetchData();
    </script>

</body>
</html>

    """

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
