from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol
from src.folder.domain.schema import Folder
from typing import List

class ListFoldersUseCase:
    def __init__(self, folder_storage_repository: FolderStorageRepositoryProtocol):
        self.folder_storage_repository = folder_storage_repository

    async def __call__(self, company_id: str) -> List[Folder]:
        return await self.folder_storage_repository.list_folders(company_id)
