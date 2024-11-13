from flask import Flask, request, jsonify
from pymongo import MongoClient

# MongoDB connection details
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "machine_data"
MONGO_COLLECTION = "machines"

app = Flask(__name__)

@app.route('/api/machines', methods=['GET'])
def get_machines():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    machines = list(collection.find())
    client.close()
    return jsonify(machines)

@app.route('/api/machines', methods=['POST'])
def create_machine():
    data = request.get_json()
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    result = collection.insert_one(data)
    client.close()
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/api/machines/<id>', methods=['GET'])
def get_machine(id):
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    machine = collection.find_one({'_id': ObjectId(id)})
    client.close()
    return jsonify(machine)

@app.route('/api/machines/<id>', methods=['PUT'])
def update_machine(id):
    data = request.get_json()
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    client.close()
    return jsonify({'modified_count': result.modified_count})

@app.route('/api/machines/<id>', methods=['DELETE'])
def delete_machine(id):
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    result = collection.delete_one({'_id': ObjectId(id)})
    client.close()
    return jsonify({'deleted_count': result.deleted_count})

if __name__ == '__main__':
    app.run(debug=True)