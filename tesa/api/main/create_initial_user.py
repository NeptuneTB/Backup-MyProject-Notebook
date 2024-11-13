from pymongo import MongoClient
from passlib.context import CryptContext
import uuid
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["machine_monitoring"]
users = db["users"]

# Setup password context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__default_rounds=12
)

def create_user():
    try:
        # Create default credentials
        username = "admin"
        password = "admin123"  # Change this to your desired password
        api_key = str(uuid.uuid4())

        # Hash password
        hashed_password = pwd_context.hash(password)

        # Create user document
        user = {
            "username": username,
            "password": hashed_password,
            "api_key": api_key,
            "created_at": datetime.utcnow()
        }

        # Check if user already exists
        existing_user = users.find_one({"username": username})
        if existing_user:
            users.update_one(
                {"username": username},
                {"$set": {
                    "password": hashed_password,
                    "api_key": api_key,
                    "updated_at": datetime.utcnow()
                }}
            )
            print(f"Updated existing user")
        else:
            users.insert_one(user)
            print(f"Created new user")

        print(f"\nUser credentials:")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"API Key: {api_key}")

    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    create_user()