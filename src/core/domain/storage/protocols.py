from typing import List, Protocol


class StorageClientProtocol(Protocol):
    def upload_file(self, source_file_name: str, destination_blob_name: str) -> None:
        """
        Upload a file to the storage bucket.

        Args:
            source_file_name (str): The path to the local file to upload.
            destination_blob_name (str): The name to give the file in the bucket.
        """
        ...

    def download_file(self, source_blob_name: str, destination_file_name: str) -> None:
        """
        Download a file from the storage bucket.

        Args:
            source_blob_name (str): The name of the file in the bucket.
            destination_file_name (str): The path where the file should be saved locally.
        """
        ...

    def delete_file(self, blob_name: str) -> None:
        """
        Delete a file from the storage bucket.

        Args:
            blob_name (str): The name of the file to delete.
        """
        ...

    def list_files(self, prefix: str = None) -> List[str]:
        """
        List files in the storage bucket.

        Args:
            prefix (str, optional): A prefix to filter the files. Defaults to None.

        Returns:
            List[str]: A list of file names in the bucket.
        """
        ...

    def get_download_link(self, blob_name: str, expiration_time: int = 3600) -> str:
        """
        Get a temporary download link for a file.

        Args:
            blob_name (str): Name of the blob in the bucket.
            expiration_time (int, optional): Link expiration time in seconds. Defaults to 3600 (1 hour).

        Returns:
            str: Temporary download URL.
        """
        ...
