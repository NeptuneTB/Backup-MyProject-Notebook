import asyncio
import websockets
import pymongo
from datetime import datetime
from flask import Flask, jsonify, request
from bson.objectid import ObjectId
import json
from flask_socketio import SocketIO

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["machine_db"]
collection = db["machine_data"]

# WebSocket client
async def receive_machine_data(api_key, socketio):
    async with websockets.connect("ws://technest.ddns.net:8001/ws") as websocket:
        await websocket.send(api_key)
        async for message in websocket:
            try:
                data = json.loads(message)
                data["timestamp"] = datetime.now()
                result = collection.insert_one(data)
                print(f"Saved data with ID: {result.inserted_id}")
                # Emit data to the front end via SocketIO
                socketio.emit('machine_data', data)
            except json.JSONDecodeError:
                print(f"Error decoding message: {message}")
            except Exception as e:
                print(f"Error saving data: {e}")

def start_websocket_client(socketio):
    api_key = "670a935a14221a12ae886117c99cacc7"
    asyncio.ensure_future(receive_machine_data(api_key, socketio))

# Flask API server
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/api/machine-data', methods=['GET'])
def get_machine_data():
    data = list(collection.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

@app.route('/api/machine-data', methods=['POST'])
def create_machine_data():
    data = request.get_json()
    data["timestamp"] = datetime.now()
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/api/machine-data/<id>', methods=['GET'])
def get_machine_data_by_id(id):
    data = collection.find_one({'_id': ObjectId(id)})
    if data:
        data['_id'] = str(data['_id'])
        return jsonify(data)
    else:
        return jsonify({'error': 'Machine data not found'}), 404

@app.route('/api/machine-data/<id>', methods=['PUT'])
def update_machine_data(id):
    data = request.get_json()
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Machine data updated'})
    else:
        return jsonify({'error': 'Machine data not found'}), 404

@app.route('/api/machine-data/<id>', methods=['DELETE'])
def delete_machine_data(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Machine data deleted'})
    else:
        return jsonify({'error': 'Machine data not found'}), 404

# Single webpage with real-time chart
@app.route('/')
def index():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Machine Monitoring Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
        </head>
        <body>
            <h1>Machine Monitoring Dashboard</h1>

            <h2>Power Consumption</h2>
            <canvas id="powerChart" width="400" height="200"></canvas>

            <h2>Voltage</h2>
            <canvas id="voltageChart" width="400" height="200"></canvas>

            <h2>Pressure</h2>
            <canvas id="pressureChart" width="400" height="200"></canvas>

            <h2>Force</h2>
            <canvas id="forceChart" width="400" height="200"></canvas>

            <h2>Cycle Count</h2>
            <canvas id="cycleCountChart" width="400" height="200"></canvas>

            <h2>Position of the Punch</h2>
            <canvas id="positionChart" width="400" height="200"></canvas>

            <script>
                var socket = io.connect('http://' + document.domain + ':' + location.port);
                
                var labels = [];
                var powerData = [];
                var voltageDataL1 = [];
                var voltageDataL2 = [];
                var voltageDataL3 = [];
                var pressureData = [];
                var forceData = [];
                var cycleCountData = [];
                var positionData = [];

                // Initialize each chart
                function createChart(elementId, label, dataset, color) {
                    return new Chart(document.getElementById(elementId), {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: label,
                                data: dataset,
                                backgroundColor: color[0],
                                borderColor: color[1],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }

                var powerChart = createChart('powerChart', 'Power Consumption', powerData, ['rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 1)']);
                var voltageChart = new Chart(document.getElementById('voltageChart'), {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            { label: 'L1-GND Voltage', data: voltageDataL1, backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)', borderWidth: 1 },
                            { label: 'L2-GND Voltage', data: voltageDataL2, backgroundColor: 'rgba(54, 162, 235, 0.2)', borderColor: 'rgba(54, 162, 235, 1)', borderWidth: 1 },
                            { label: 'L3-GND Voltage', data: voltageDataL3, backgroundColor: 'rgba(153, 102, 255, 0.2)', borderColor: 'rgba(153, 102, 255, 1)', borderWidth: 1 }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
                });
                var pressureChart = createChart('pressureChart', 'Pressure', pressureData, ['rgba(255, 159, 64, 0.2)', 'rgba(255, 159, 64, 1)']);
                var forceChart = createChart('forceChart', 'Force', forceData, ['rgba(255, 206, 86, 0.2)', 'rgba(255, 206, 86, 1)']);
                var cycleCountChart = createChart('cycleCountChart', 'Cycle Count', cycleCountData, ['rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 1)']);
                var positionChart = createChart('positionChart', 'Position of the Punch', positionData, ['rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 1)']);

                // Update charts with new data
                socket.on('machine_data', function(data) {
                    var timestamp = new Date(data.timestamp).toLocaleTimeString();
                    labels.push(timestamp);
                    powerData.push(data['Energy Consumption'].Power);
                    voltageDataL1.push(data['Voltage']['L1-GND']);
                    voltageDataL2.push(data['Voltage']['L2-GND']);
                    voltageDataL3.push(data['Voltage']['L3-GND']);
                    pressureData.push(data.Pressure);
                    forceData.push(data.Force);
                    cycleCountData.push(data['Cycle Count']);
                    positionData.push(data['Position of the Punch']);

                    // Update each chart
                    powerChart.update();
                    voltageChart.update();
                    pressureChart.update();
                    forceChart.update();
                    cycleCountChart.update();
                    positionChart.update();
                });
            </script>
        </body>
        </html>
    """

if __name__ == '__main__':
    start_websocket_client(socketio)  # Start WebSocket client to fetch data
    socketio.run(app, debug=True)
