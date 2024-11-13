from flask import Flask, jsonify, request
from bson import ObjectId
from database import insert_machine_data, get_all_machine_data, update_machine_data, delete_machine_data

app = Flask(__name__)
API_KEY = "670a935a14221a12ae886117c99cacc7"

def verify_api_key(api_key):
    return api_key == API_KEY

@app.route('/api/machine', methods=['POST'])
def create_machine_data():
    if not verify_api_key(request.headers.get("apikey")):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    insert_machine_data(data)
    return jsonify({"message": "Data added successfully"}), 201

@app.route('/api/machine', methods=['GET'])
def get_machine_data():
    data = get_all_machine_data()
    return jsonify(data)

@app.route('/api/machine/<id>', methods=['PUT'])
def update_machine_data_endpoint(id):
    if not verify_api_key(request.headers.get("apikey")):
        return jsonify({"error": "Unauthorized"}), 401
    new_data = request.json
    update_machine_data(ObjectId(id), new_data)
    return jsonify({"message": "Data updated successfully"})

@app.route('/api/machine/<id>', methods=['DELETE'])
def delete_machine_data_endpoint(id):
    if not verify_api_key(request.headers.get("apikey")):
        return jsonify({"error": "Unauthorized"}), 401
    delete_machine_data(ObjectId(id))
    return jsonify({"message": "Data deleted successfully"})
