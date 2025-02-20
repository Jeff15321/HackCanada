from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

async def get_database() -> AsyncIOMotorClient:
    """
    Get database connection
    """
    print("Getting database:", Database.db)
    if Database.db is None:
        print("Database connection not initialized!")
        await connect_to_mongo()
    return Database.db

async def connect_to_mongo():
    """
    Connect to MongoDB
    """
    try:
        print("Connecting to MongoDB URL:", settings.MONGODB_URL)
        Database.client = AsyncIOMotorClient(settings.MONGODB_URL)
        Database.db = Database.client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB Atlas!")
        # Test the connection
        await Database.client.admin.command('ping')
        print("Pinged database successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """
    Close MongoDB connection
    """
    if Database.client:
        Database.client.close()
        print("MongoDB connection closed!") 