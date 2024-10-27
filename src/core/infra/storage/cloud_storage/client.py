import json
from datetime import datetime, timedelta, timezone

from google.cloud import storage
from google.oauth2 import service_account

from src.core.domain.storage.protocols import StorageClientProtocol


class CloudStorageClient(StorageClientProtocol):
    """
    A client for interacting with Google Cloud Storage.

    This class provides methods for common operations such as uploading,
    downloading, and deleting files, as well as listing files and generating
    download links.
    """

    def __init__(self, bucket_name: str, project_id: str):
        """
        Initialize the CloudStorageClient.

        Args:
            bucket_name (str): The name of the storage bucket.
        """
        with open("credentials_google.json", "r") as credentials_file:
            credentials_info = json.load(credentials_file)

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )
        self.client = storage.Client(
            credentials=credentials, project=credentials_info["project_id"]
        )
        self.bucket = self.client.bucket(bucket_name)

    async def upload_file(
        self, file_content: bytes, destination_blob_name: str, content_type: str
    ):
        """
        Upload a file to the storage bucket.

        Args:
            file_content (bytes): The content of the file to upload.
            destination_blob_name (str): The name to give the file in the bucket.
            content_type (str): The MIME type of the file.
        """
        bucket = self.bucket
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(file_content, content_type=content_type)

    async def download_file(self, source_blob_name: str, destination_file_name: str):
        """
        Download a file from the storage bucket.

        Args:
            source_blob_name (str): The name of the file in the bucket.
            destination_file_name (str): The path where the file should be saved locally.
        """
        blob = self.bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

    async def delete_file(self, blob_name: str):
        """
        Delete a file from the storage bucket.

        Args:
            blob_name (str): The name of the file to delete.
        """
        blob = self.bucket.blob(blob_name)
        blob.delete()
        (f"File {blob_name} deleted.")

    async def list_files(self, prefix: str = None):
        """
        List files in the storage bucket.

        Args:
            prefix (str, optional): A prefix to filter the files. Defaults to None.

        Returns:
            list: A list of file names in the bucket.
        """
        blobs = self.bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    async def get_download_link(self, blob_name: str, expiration_time: int = 3600):
        """
        Get a temporary download link for a file.

        Args:
            blob_name (str): Name of the blob in the bucket.
            expiration_time (int, optional): Link expiration time in seconds. Defaults to 3600 (1 hour).

        Returns:
            str: Temporary download URL.
        """
        blob = self.bucket.blob(blob_name)
        expiration_datetime = datetime.now(timezone.utc) + timedelta(
            seconds=expiration_time
        )
        url = blob.generate_signed_url(expiration=expiration_datetime)
        return url
