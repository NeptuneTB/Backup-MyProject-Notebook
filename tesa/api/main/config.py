from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "machine_monitoring"
COLLECTION_NAME = "machine_data"
USERS_COLLECTION = "users"

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # ในการใช้งานจริงควรเก็บไว้ใน environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30