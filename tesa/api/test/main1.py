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
            <script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js"></script>
        </head>
        <body>
            <h1>Machine Monitoring Dashboard</h1>

            <!-- Separate canvases for each metric -->
            <h2>Power</h2>
            <canvas id="powerChart"></canvas>
            
            <h2>L1-GND Voltage</h2>
            <canvas id="voltageL1Chart"></canvas>

            <h2>L2-GND Voltage</h2>
            <canvas id="voltageL2Chart"></canvas>

            <h2>L3-GND Voltage</h2>
            <canvas id="voltageL3Chart"></canvas>

            <h2>Pressure</h2>
            <canvas id="pressureChart"></canvas>

            <h2>Force</h2>
            <canvas id="forceChart"></canvas>

            <h2>Position of the Punch</h2>
            <canvas id="positionChart"></canvas>

            <script>
                var ws;
                var timeLabels = [];

                // Create chart configurations
                var createChartConfig = function(label, borderColor, backgroundColor) {
                    return {
                        type: 'line',
                        data: {
                            labels: timeLabels,
                            datasets: [{
                                label: label,
                                data: [],
                                borderColor: borderColor,
                                backgroundColor: backgroundColor,
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
                    };
                };

                // Initialize charts
                var powerChart = new Chart(document.getElementById('powerChart'), createChartConfig('Power', 'rgba(255, 99, 132, 1)', 'rgba(255, 99, 132, 0.2)'));
                var voltageL1Chart = new Chart(document.getElementById('voltageL1Chart'), createChartConfig('L1-GND Voltage', 'rgba(54, 162, 235, 1)', 'rgba(54, 162, 235, 0.2)'));
                var voltageL2Chart = new Chart(document.getElementById('voltageL2Chart'), createChartConfig('L2-GND Voltage', 'rgba(75, 192, 192, 1)', 'rgba(75, 192, 192, 0.2)'));
                var voltageL3Chart = new Chart(document.getElementById('voltageL3Chart'), createChartConfig('L3-GND Voltage', 'rgba(153, 102, 255, 1)', 'rgba(153, 102, 255, 0.2)'));
                var pressureChart = new Chart(document.getElementById('pressureChart'), createChartConfig('Pressure', 'rgba(255, 206, 86, 1)', 'rgba(255, 206, 86, 0.2)'));
                var forceChart = new Chart(document.getElementById('forceChart'), createChartConfig('Force', 'rgba(75, 192, 192, 1)', 'rgba(75, 192, 192, 0.2)'));
                var positionChart = new Chart(document.getElementById('positionChart'), createChartConfig('Position of the Punch', 'rgba(255, 159, 64, 1)', 'rgba(255, 159, 64, 0.2)'));

                function connect() {
                    var apiKey = "670a935a14221a12ae886117c99cacc7";
                    ws = new WebSocket("ws://technest.ddns.net:8001/ws");
                    ws.onopen = function(event) {
                        ws.send(apiKey);
                    };
                    
                    ws.onclose = function(event) {
                        console.log("WebSocket closed, reconnecting...");
                        setTimeout(connect, 1000); // Reconnect after 1 second
                    };

                    var MAX_POINTS = 50;

                    ws.onmessage = function(event) {
                        var data = JSON.parse(event.data);
                        var timestamp = new Date(data.timestamp).toLocaleTimeString();
                        
                        if (timeLabels.length >= MAX_POINTS) {
                            timeLabels.shift(); // Remove oldest label
                            powerChart.data.datasets[0].data.shift();
                            voltageL1Chart.data.datasets[0].data.shift();
                            voltageL2Chart.data.datasets[0].data.shift();
                            voltageL3Chart.data.datasets[0].data.shift();
                            pressureChart.data.datasets[0].data.shift();
                            forceChart.data.datasets[0].data.shift();
                            positionChart.data.datasets[0].data.shift();
                        }

                        // Add new data points
                        timeLabels.push(timestamp);
                        powerChart.data.datasets[0].data.push(data["Energy Consumption"].Power);
                        voltageL1Chart.data.datasets[0].data.push(data.Voltage["L1-GND"]);
                        voltageL2Chart.data.datasets[0].data.push(data.Voltage["L2-GND"]);
                        voltageL3Chart.data.datasets[0].data.push(data.Voltage["L3-GND"]);
                        pressureChart.data.datasets[0].data.push(data.Pressure);
                        forceChart.data.datasets[0].data.push(data.Force);
                        positionChart.data.datasets[0].data.push(data["Position of the Punch"]);

                        // Update each chart
                        powerChart.update();
                        voltageL1Chart.update();
                        voltageL2Chart.update();
                        voltageL3Chart.update();
                        pressureChart.update();
                        forceChart.update();
                        positionChart.update();
                    };
                }
                
                if (timeLabels.length > 50) {
                    timeLabels.shift();
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