from src.folder.domain.schema import Folder
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol


class UploadFolderUseCase:
    def __init__(self, folder_storage_repository: FolderStorageRepositoryProtocol):
        self.folder_storage_repository = folder_storage_repository

    async def __call__(self, company_id: str, folder: Folder, content: bytes, content_type: str) -> Folder:
        return await self.folder_storage_repository.save_folder(folder, company_id, content, content_type)
