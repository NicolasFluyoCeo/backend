from typing import List, Protocol

from src.folder.domain.schema import FolderRepositorySchema


class FolderRepositoryInterface(Protocol):
    async def create_folder(self, folder: FolderRepositorySchema) -> str:
        """
        Create a new folder for a company.

        Args:
            company_id (str): The ID of the company.

        Returns:
            str: The ID of the created folder.
        """
        ...

    async def list_folders(self, company_id: str) -> List[FolderRepositorySchema]:
        """
        List all folders for a company.

        Args:
            company_id (str): The ID of the company.

        Returns:
            List[Folder]: A list of Folder objects.
        """
        ...

    async def get_folder(
        self, company_id: str, folder_id: str
    ) -> FolderRepositorySchema:
        """
        Get a specific folder for a company.

        Args:
            company_id (str): The ID of the company.
            folder_id (str): The ID of the folder.

        Returns:
            Folder: The requested Folder object.
        """
        ...

    async def update_folder(
        self, company_id: str, folder_id: str, folder: FolderRepositorySchema
    ) -> FolderRepositorySchema:
        """
        Update a specific folder for a company.

        Args:
            company_id (str): The ID of the company.
            folder_id (str): The ID of the folder to update.
            folder (Folder): The updated Folder object.

        Returns:
            Folder: The updated Folder object.
        """
        ...

    async def delete_folder(self, company_id: str, folder_id: str) -> bool:
        """
        Delete a specific folder for a company.

        Args:
            company_id (str): The ID of the company.
            folder_id (str): The ID of the folder to delete.

        Returns:
            bool: True if the folder was successfully deleted, False otherwise.
        """
        ...
