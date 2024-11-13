import asyncio
import websockets
import pymongo
from datetime import datetime
from flask import Flask, jsonify, request
from bson.objectid import ObjectId
import json

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["machine_db"]
collection = db["machine_data"]

# WebSocket client
async def receive_machine_data(api_key):
    async with websockets.connect("ws://technest.ddns.net:8001/ws") as websocket:
        await websocket.send(api_key)
        async for message in websocket:
            try:
                data = json.loads(message)
                data["timestamp"] = datetime.now()
                result = collection.insert_one(data)
                print(f"Saved data with ID: {result.inserted_id}")
            except json.JSONDecodeError:
                print(f"Error decoding message: {message}")
            except Exception as e:
                print(f"Error saving data: {e}")

def run_websocket_client():
    api_key = "670a935a14221a12ae886117c99cacc7"
    asyncio.get_event_loop().run_until_complete(receive_machine_data(api_key))

# Flask API server
app = Flask(__name__)

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
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Machine Monitoring Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>Machine Monitoring Dashboard</h1>
            <canvas id="myChart"></canvas>

            <script>
                var ws;
                var chartData = {
                    labels: [],
                    datasets: [{
                        label: 'Temperature',
                        data: [],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                };

                var myChart = new Chart(document.getElementById('myChart'), {
                    type: 'line',
                    data: chartData,
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

                function connect() {
                    var apiKey = "670a935a14221a12ae886117c99cacc7";
                    ws = new WebSocket("ws://technest.ddns.net:8001/ws");
                    ws.onopen = function(event) {
                        ws.send(apiKey);
                    };
                    ws.onmessage = function(event) {
                        var data = JSON.parse(event.data);
                        chartData.labels.push(data.timestamp);
                        chartData.datasets[0].data.push(data.temperature);
                        myChart.update();
                    };
                }

                connect();
            </script>
        </body>
        </html>
    '''

if __name__ == '__main__':
    run_websocket_client()
    app.run(debug=True)