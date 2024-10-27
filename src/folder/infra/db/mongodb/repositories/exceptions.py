
class FolderRepositoryException(Exception):
    """Base exception for folder repository errors."""
    pass

class FolderAlreadyExistsException(FolderRepositoryException):
    """Raised when attempting to create a folder that already exists."""
    def __init__(self, company_id: str, folder_name: str):
        self.message = f"Folder '{folder_name}' already exists for company with ID '{company_id}'."
        super().__init__(self.message)

class FolderNotFoundException(FolderRepositoryException):
    """Raised when a specific folder is not found."""
    def __init__(self, company_id: str, folder_id: str):
        self.message = f"Folder with ID '{folder_id}' not found for company with ID '{company_id}'."
        super().__init__(self.message)

class FolderUpdateException(FolderRepositoryException):
    """Raised when there's an error updating a folder."""
    def __init__(self, company_id: str, folder_id: str):
        self.message = f"Error updating folder with ID '{folder_id}' for company with ID '{company_id}'."
        super().__init__(self.message)

class FolderCreationException(FolderRepositoryException):
    """Raised when there's an error creating a folder."""
    def __init__(self, company_id: str):
        self.message = f"Error creating a new folder for company with ID '{company_id}'."
        super().__init__(self.message)

class FolderListException(FolderRepositoryException):
    """Raised when there's an error listing folders."""
    def __init__(self, company_id: str):
        self.message = f"Error listing folders for company with ID '{company_id}'."
        super().__init__(self.message)

