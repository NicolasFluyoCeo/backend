from src.folder.application.use_cases.upload_folder.use_case import UploadFolderUseCase
from src.folder.domain.schema import Folder
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol


class FolderService:
    def __init__(self, folder_storage_repository: FolderStorageRepositoryProtocol):
        self.folder_storage_repository = folder_storage_repository

    async def upload_folder(self, company_id: str, file: Folder) -> None:
        use_case = UploadFolderUseCase(self.folder_storage_repository)
        await use_case(company_id, file)
