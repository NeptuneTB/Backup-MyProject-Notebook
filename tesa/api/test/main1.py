import asyncio
import websockets
import pymongo
from datetime import datetime
from flask import Flask, jsonify, request
from bson.objectid import ObjectId
import json
import threading

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

def start_websocket_client():
    api_key = "670a935a14221a12ae886117c99cacc7"
    asyncio.run(receive_machine_data(api_key))

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
# The Flask server and the WebSocket client code remain the same.
# Update the HTML and JavaScript in the `index()` route:

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
                    datasets: [
                        {
                            label: 'Power',
                            data: [],
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'L1-GND Voltage',
                            data: [],
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'L2-GND Voltage',
                            data: [],
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'L3-GND Voltage',
                            data: [],
                            backgroundColor: 'rgba(153, 102, 255, 0.2)',
                            borderColor: 'rgba(153, 102, 255, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'Pressure',
                            data: [],
                            backgroundColor: 'rgba(255, 206, 86, 0.2)',
                            borderColor: 'rgba(255, 206, 86, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'Force',
                            data: [],
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'Position of the Punch',
                            data: [],
                            backgroundColor: 'rgba(255, 159, 64, 0.2)',
                            borderColor: 'rgba(255, 159, 64, 1)',
                            borderWidth: 1
                        }
                    ]
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

                        var timestamp = new Date(data.timestamp).toLocaleTimeString();
                        chartData.labels.push(timestamp);
                        
                        // Adding data points to each dataset
                        chartData.datasets[0].data.push(data["Energy Consumption"].Power);
                        chartData.datasets[1].data.push(data.Voltage["L1-GND"]);
                        chartData.datasets[2].data.push(data.Voltage["L2-GND"]);
                        chartData.datasets[3].data.push(data.Voltage["L3-GND"]);
                        chartData.datasets[4].data.push(data.Pressure);
                        chartData.datasets[5].data.push(data.Force);
                        chartData.datasets[6].data.push(data["Position of the Punch"]);

                        // Update the chart
                        myChart.update();
                    };
                }

                connect();
            </script>
        </body>
        </html>
    '''

if __name__ == '__main__':
    # Start the WebSocket client in a separate thread
    websocket_thread = threading.Thread(target=start_websocket_client)
    websocket_thread.start()

    # Start the Flask app
    app.run(debug=True)