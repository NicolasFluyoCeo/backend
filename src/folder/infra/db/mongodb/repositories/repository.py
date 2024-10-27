from datetime import datetime, timezone
from typing import List

from src.core.infra.db.mongodb.repository import MongoDBRepositoryImpl
from src.folder.domain.repository import FolderRepositoryInterface
from src.folder.domain.schema import FolderRepositorySchema
from src.folder.infra.db.mongodb.repositories.exceptions import (
    FolderAlreadyExistsException,
    FolderCreationException,
    FolderListException,
    FolderNotFoundException,
    FolderUpdateException,
)


class FolderRepositoryImpl(FolderRepositoryInterface):
    def __init__(self, mongodb_repository: MongoDBRepositoryImpl):
        self._mongodb_repository = mongodb_repository
        self._collection = "folders"

    async def create_folder(
        self,
        folder: FolderRepositorySchema,
    ) -> FolderRepositorySchema:
        existing_folder = await self._mongodb_repository.find_one(
            self._collection, {"company_id": folder.company_id, "name": folder.name}
        )
        if existing_folder:
            raise FolderAlreadyExistsException(folder.company_id, folder.name)

        folder.created_at = datetime.now(timezone.utc)
        folder.updated_at = datetime.now(timezone.utc)
        folder_dict = folder.model_dump(exclude={"_id"})
        try:
            folder_data = await self._mongodb_repository.insert_one(
                self._collection, folder_dict
            )
            return FolderRepositorySchema.model_validate(
                {"_id": str(folder_data.inserted_id), **folder_dict}
            )
        except Exception:
            raise FolderCreationException(folder.company_id)

    async def list_folders(self, company_id: str) -> List[FolderRepositorySchema]:
        try:
            folders = await self._mongodb_repository.find_many(
                self._collection, {"company_id": company_id}
            )
            return [
                FolderRepositorySchema(id=str(folder["_id"]), **folder)
                for folder in folders
            ]
        except Exception:
            raise FolderListException(company_id)

    async def get_folder(
        self, company_id: str, folder_id: str
    ) -> FolderRepositorySchema:
        folder = await self._mongodb_repository.find_one(
            self._collection, {"company_id": company_id, "_id": folder_id}
        )
        if not folder:
            raise FolderNotFoundException(company_id, folder_id)
        return FolderRepositorySchema(id=str(folder["_id"]), **folder)

    async def update_folder(
        self, company_id: str, folder_id: str, folder: FolderRepositorySchema
    ) -> FolderRepositorySchema:
        try:
            updated_folder = await self._mongodb_repository.update_one(
                self._collection, {"company_id": company_id, "_id": folder_id}, folder
            )
            if not updated_folder:
                raise FolderNotFoundException(company_id, folder_id)
            return FolderRepositorySchema(
                id=str(updated_folder["_id"]), **updated_folder
            )
        except Exception:
            raise FolderUpdateException(company_id, folder_id)
