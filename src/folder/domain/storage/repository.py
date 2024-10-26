from typing import List, Protocol

from src.folder.domain.schema import Folder


class FolderStorageRepositoryProtocol(Protocol):
    async def save_folder(self, folder: Folder, company_id: str) -> None:
        """
        Saves a folder to the storage.

        Args:
            folder (Folder): The folder to save.
            company_id (str): The ID of the company.

        The storage path would be: folders/{company_id}/{folder.path}/{folder.name}
        """
        ...

    async def get_folder(self, company_id: str, name: str) -> Folder:
        """
        Retrieves a folder from the storage.

        Args:
            company_id (str): The ID of the company.
            name (str): The name of the folder.

        Returns:
            Folder: The retrieved folder.

        The storage path would be: folders/{company_id}/{path}/{name}
        """
        ...

    async def delete_folder(self, company_id: str, name: str) -> None:
        """
        Deletes a folder from the storage.

        Args:
            company_id (str): The ID of the company.
            path (str): The path of the folder.
            name (str): The name of the folder.

        The storage path would be: folders/{company_id}/{path}/{name}
        """
        ...

    async def list_folders(self, company_id: str) -> List[Folder]:
        """
        Lists all folders for a company.
        """
        ...
