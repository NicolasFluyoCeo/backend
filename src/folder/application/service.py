from typing import List

from src.folder.application.use_cases.list_folders.use_case import ListFoldersUseCase
from src.folder.application.use_cases.upload_folder.use_case import UploadFolderUseCase
from src.folder.domain.schema import Folder
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol


class FolderService:
    def __init__(self, folder_storage_repository: FolderStorageRepositoryProtocol):
        self.folder_storage_repository = folder_storage_repository

    async def upload_folder(self, company_id: str, folder: Folder, content: bytes, content_type: str) -> None:
        use_case = UploadFolderUseCase(self.folder_storage_repository)
        await use_case(company_id, folder, content, content_type)

    async def list_folders(self, company_id: str) -> List[Folder]:
        use_case = ListFoldersUseCase(self.folder_storage_repository)
        return await use_case(company_id)
