from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["machine_db"]
machine_data_collection = db["machine_data"]

def insert_machine_data(data):
    machine_data_collection.insert_one(data)

def get_all_machine_data():
    return list(machine_data_collection.find())

def update_machine_data(record_id, new_data):
    machine_data_collection.update_one({"_id": record_id}, {"$set": new_data})

def delete_machine_data(record_id):
    machine_data_collection.delete_one({"_id": record_id})
