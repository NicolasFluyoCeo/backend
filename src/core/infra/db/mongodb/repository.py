from datetime import datetime, timezone
from typing import Any, List, Optional

import jwt
from bson import ObjectId

from src.core.domain.db.schema import MongoDBRepository
from src.core.infra.db.mongodb.client import Client


class MongoDBRepositoryImpl(MongoDBRepository):
    def __init__(self, client: Client):
        self._client = client
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            await self._connect()
            self._initialized = True

    async def _connect(self):
        await self._client.connect()

    async def disconnect(self) -> None:
        await self._client.close()
        self._initialized = False

    async def insert_one(self, collection: str, document: dict) -> Any:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        return await collection.insert_one(document)

    async def insert_many(self, collection: str, documents: List[dict]) -> Any:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        return await collection.insert_many(documents)

    async def find_one(self, collection: str, query: dict) -> dict:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])
        return await collection.find_one(query)

    async def find_many(self, collection: str, query: dict) -> List[dict]:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])
        cursor = collection.find(query)
        return await cursor.to_list(length=None)

    async def update_one(self, collection: str, query: dict, update: dict) -> Any:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])
        return await collection.update_one(query, update)

    async def update_many(self, collection: str, query: dict, update: dict) -> Any:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])
        return await collection.update_many(query, update)

    async def delete_one(self, collection: str, query: dict) -> Any:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])
        return await collection.delete_one(query)

    async def delete_many(self, collection: str, query: dict) -> Any:
        await self.initialize()
        collection = await self._client.get_collection(collection)
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])
        return await collection.delete_many(query)


class SessionTokenRepositoryImpl:
    def __init__(self, mongodb_repository: MongoDBRepositoryImpl):
        self._mongodb_repository = mongodb_repository
        self._session_collection = "sessions"
        self._token_collection = "sessions"
        self._secret_key = (
            "SECRET_KEY"  # Asegúrate de usar una clave secreta segura en producción
        )

    async def create_session(self, session_data: dict) -> str:
        # Revocar sesiones anteriores del usuario
        await self.revoke_previous_sessions(session_data["user_id"])

        session_data["created_at"] = datetime.now(timezone.utc)
        result = await self._mongodb_repository.insert_one(
            self._session_collection, session_data
        )
        return str(result.inserted_id)

    async def get_session(self, session_id: str) -> Optional[dict]:
        return await self._mongodb_repository.find_one(
            self._session_collection, {"_id": session_id}
        )

    async def update_session(self, session_id: str, update_data: dict) -> bool:
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = await self._mongodb_repository.update_one(
            self._session_collection, {"_id": session_id}, {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_session(self, session_id: str) -> bool:
        result = await self._mongodb_repository.delete_one(
            self._session_collection, {"_id": session_id}
        )
        return result.deleted_count > 0

    async def store_jwt_token(self, token_data: dict) -> str:
        # Revocar tokens anteriores del usuario
        await self.revoke_previous_tokens(token_data["user_id"])

        # Crear un nuevo token JWT
        new_token = jwt.encode(token_data, self._secret_key, algorithm="HS256")

        token_data["token"] = new_token
        token_data["created_at"] = datetime.now(timezone.utc)
        result = await self._mongodb_repository.insert_one(
            self._token_collection, token_data
        )
        return new_token

    async def get_jwt_token(self, token: str) -> Optional[dict]:
        result = await self._mongodb_repository.find_one(
            self._token_collection, {"token": token}
        )
        if result is None:
            # Buscar el token en la colección completa para depuración
            all_tokens = await self._mongodb_repository.find_many(
                self._token_collection, {}
            )
        return result

    async def revoke_jwt_token(self, token: str) -> bool:
        result = await self._mongodb_repository.update_one(
            self._token_collection,
            {"token": token},
            {"$set": {"revoked": True, "revoked_at": datetime.now(timezone.utc)}},
        )
        return result.modified_count > 0

    async def validate_session(self, token: str) -> bool:
        session = await self.get_session(token)
        return session is not None and not session.get("revoked", False)

    async def revoke_previous_sessions(self, user_id: str) -> None:
        await self._mongodb_repository.update_many(
            self._session_collection,
            {"user_id": user_id, "revoked": {"$ne": True}},
            {"$set": {"revoked": True, "revoked_at": datetime.now(timezone.utc)}},
        )

    async def revoke_previous_tokens(self, user_id: str) -> None:
        await self._mongodb_repository.update_many(
            self._token_collection,
            {"user_id": user_id, "revoked": {"$ne": True}},
            {"$set": {"revoked": True, "revoked_at": datetime.now(timezone.utc)}},
        )
