from src.folder.domain.repository import FolderRepositoryInterface
from src.folder.domain.schema import FolderRepositorySchema

class GetFolderUseCase:
    def __init__(self, folder_repository: FolderRepositoryInterface):
        self.folder_repository = folder_repository

    async def __call__(self, company_id: str, folder_id: str) -> FolderRepositorySchema:
        return await self.folder_repository.get_folder(company_id, folder_id)
