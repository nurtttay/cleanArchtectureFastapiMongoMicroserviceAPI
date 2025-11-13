import os
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self):
        self.client = None
        self._db = None

    async def db(self):
        if self._db is None:
            uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/?replicaSet=rs0")
            db_name = os.getenv("DB_NAME", "testdb")
            self.client = AsyncIOMotorClient(uri)
            self._db = self.client[db_name]
        return self._db