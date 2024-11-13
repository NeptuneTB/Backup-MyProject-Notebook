# database.py
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.weather_db
collection = db.weather_data

def save_data(data):
    if isinstance(data, dict):  # ตรวจสอบว่า data เป็น dict หรือไม่
        collection.insert_one(data)
        print(f"Data saved to MongoDB: {data}")
    else:
        print("Data is not in valid format. It must be a dictionary.")
