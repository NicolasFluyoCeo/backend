from typing import List

from src.core.domain.storage.protocols import StorageClientProtocol
from src.folder.domain.schema import File, Folder, FileNameDescriptionUrl
from src.folder.domain.storage.repository import FolderStorageRepositoryProtocol


class FolderStorageRepository(FolderStorageRepositoryProtocol):
    def __init__(self, storage_client: StorageClientProtocol):
        self.storage_client = storage_client

    async def save_folder(self, folder: Folder, company_id: str, content: bytes, content_type: str):
        path = f"folders/{company_id}/{folder.file.name}"
        await self.storage_client.upload_file(
            content, path, content_type
        )
        url = await self.storage_client.get_download_link(path)
        folder.file = FileNameDescriptionUrl(
            name=folder.file.name,
            description=folder.description,
            url=url
        )
        return folder

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
        folders = []
        for file in files:
            try:
                url = await self.storage_client.get_download_link(f"{file}")  # Cambiado de f"{path}/{file}" a f"{file}"
                file_info = FileNameDescriptionUrl(
                    name=file,
                    description="",  # Puedes ajustar esto si tienes una forma de obtener la descripción
                    url=url
                )
                folders.append(Folder(file=file_info, description=""))
            except Exception as e:
                print(f"Error al procesar el archivo {file}: {str(e)}")
                continue  # Salta al siguiente archivo si hay un error
        return folders
