from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from pydantic import EmailStr

from src.core.infra.db.mongodb.repository import MongoDBRepositoryImpl
from src.users.domain.schema import (
    UserDataInterface,
    UserInterface,
    UserReadInterface,
    UserRepository,
)


class UserRepositoryImpl(UserRepository):
    def __init__(self, mongodb_repository: MongoDBRepositoryImpl):
        self._mongodb_repository = mongodb_repository
        self._collection = "users"

    async def get_user_by_email(self, email: EmailStr) -> Optional[UserInterface]:
        user_data = await self._mongodb_repository.find_one(
            self._collection, {"email": email}
        )
        return (
            UserInterface(
                id=str(user_data["_id"]),
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                is_active=user_data["is_active"],
                cell_phone=user_data.get("cell_phone", ""),
                password=user_data["password"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"],
            )
            if user_data
            else None
        )

    async def get_user_by_id(self, user_id: str) -> Optional[UserInterface]:
        user_data = await self._mongodb_repository.find_one(
            self._collection, {"_id": ObjectId(user_id)}
        )
        return self._create_user_interface(user_data) if user_data else None

    async def update_user(self, user: UserInterface) -> UserInterface:
        update_data = {
            "$set": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "updated_at": user.updated_at,
            }
        }
        await self._mongodb_repository.update_one(
            self._collection, {"_id": ObjectId(user.id)}, update_data
        )
        return user

    async def delete_user(self, user_id: str) -> bool:
        result = await self._mongodb_repository.delete_one(
            self._collection, {"_id": ObjectId(user_id)}
        )
        return result.deleted_count > 0

    async def get_all_users(self) -> List[UserInterface]:
        users_data = await self._mongodb_repository.find_many(self._collection, {})
        return [self._create_user_interface(user_data) for user_data in users_data]

    async def create_user(self, user_data: UserDataInterface) -> UserInterface:
        new_user = {
            "username": user_data.username,
            "email": user_data.email,
            "password": user_data.password,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "is_active": False,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "role": user_data.role.value,
        }
        result = await self._mongodb_repository.insert_one(self._collection, new_user)
        new_user["_id"] = result.inserted_id
        return self._create_user_interface(new_user)

    def _create_user_interface(self, user_data: dict) -> UserReadInterface:
        return UserReadInterface(
            id=str(user_data["_id"]),
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            is_active=user_data["is_active"],
            cell_phone=user_data.get("cell_phone", ""),
        )
