from src.folder.domain.repository import FolderRepositoryInterface
from src.folder.domain.schema import Folder, FolderRepositorySchema
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol


class UploadFolderUseCase:
    def __init__(
        self,
        folder_storage_repository: FolderStorageRepositoryProtocol,
        folder_repository: FolderRepositoryInterface,
    ):
        self.folder_storage_repository = folder_storage_repository
        self.folder_repository = folder_repository

    async def __call__(
        self, company_id: str, folder: Folder, content: bytes, content_type: str
    ) -> Folder:
        data = await self.folder_storage_repository.save_folder(
            folder, company_id, content, content_type
        )
        db_data = FolderRepositorySchema(
            company_id=company_id,
            name=folder.file.name,
            description=folder.description,
            path=data.file.path,
        )
        await self.folder_repository.create_folder(db_data)

        return data
