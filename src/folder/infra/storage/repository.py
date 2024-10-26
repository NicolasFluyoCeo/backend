from typing import List

from src.core.domain.storage.protocols import StorageClientProtocol
from src.folder.domain.schema import Folder
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol


class FolderStorageRepository(FolderStorageRepositoryProtocol):
    def __init__(self, storage_client: StorageClientProtocol):
        self.storage_client = storage_client

    async def save_folder(self, folder: Folder, company_id: str):
        path = f"folders/{company_id}/{folder.file.name}"
        await self.storage_client.upload_file(folder.file.content, path, folder.file.mimetype)

    async def get_folder(self, company_id: str, name: str) -> Folder:
        path = f"folders/{company_id}/{name}"
        file = await self.storage_client.download_file(path)
        return Folder(file=file)

    async def delete_folder(self, company_id: str, name: str) -> None:
        path = f"folders/{company_id}/{name}"
        await self.storage_client.delete_file(path)

    async def list_folders(self, company_id: str) -> List[Folder]:
        path = f"folders/{company_id}"
        files = await self.storage_client.list_files(path)
        return [Folder(file=file) for file in files]