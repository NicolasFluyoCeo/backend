from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Client:
    def __init__(self, connection_string: str, database_name: str):
        self._client: Optional[AsyncIOMotorClient] = None
        self._db = None
        self._connection_string = connection_string
        self._database_name = database_name
        self._initialized = False

    async def connect(self):
        if not self._initialized:
            self._client = AsyncIOMotorClient(self._connection_string)
            self._db = self._client[self._database_name]
            self._initialized = True

    async def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            self._initialized = False

    async def get_database(self):
        if not self._initialized:
            await self.connect()
        return self._db

    async def get_collection(self, collection_name: str):
        db = await self.get_database()
        return db[collection_name]
