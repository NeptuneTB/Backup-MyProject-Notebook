from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DATABASE_NAME, COLLECTION_NAME, USERS_COLLECTION

class Database:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(MONGODB_URL)
        
    @classmethod
    async def close_db(cls):
        if cls.client:
            await cls.client.close()
            
    @classmethod
    async def get_collection(cls):
        database = cls.client[DATABASE_NAME]
        return database[COLLECTION_NAME]
    
    @classmethod
    async def get_users_collection(cls):
        database = cls.client[DATABASE_NAME]
        return database[USERS_COLLECTION]
