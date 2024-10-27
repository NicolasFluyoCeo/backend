from typing import List

from src.folder.domain.schema import Folder
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol
from src.folder.infra.db.mongodb.repositories.repository import (
    FolderRepositoryInterface,
)


class ListFoldersUseCase:
    def __init__(
        self,
        folder_storage_repository: FolderStorageRepositoryProtocol,
        folder_repository: FolderRepositoryInterface,
    ):
        self.folder_storage_repository = folder_storage_repository
        self.folder_repository = folder_repository

    async def __call__(self, company_id: str) -> List[Folder]:
        folders = await self.folder_repository.list_folders(company_id)

        for folder in folders:
            if folder.path:
                url = await self.folder_storage_repository.get_url(folder.path)
                folder.path = url

        return folders
