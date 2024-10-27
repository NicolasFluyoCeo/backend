from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.company.application.service import CompanyService
from src.company.infra.db.mongodb.repoitories.repository import CompanyRepositoryImpl
from src.core.infra.db.mongodb.client import Client as MongoDBClient
from src.core.infra.db.mongodb.repository import (
    MongoDBRepositoryImpl,
    SessionTokenRepositoryImpl,
)
from src.core.infra.storage.cloud_storage.client import CloudStorageClient
from src.folder.application.service import FolderService
from src.folder.infra.db.mongodb.repositories.repository import FolderRepositoryImpl
from src.folder.infra.storage.repository import FolderStorageRepository
from src.presentation.api.di.stub import (
    get_company_repository_stub,
    get_folder_repository_stub,
    get_folder_storage_repository_stub,
    get_mongodb_repository_stub,
    get_session_token_repository_stub,
    get_user_repository_stub,
    get_user_service_stub,
)
from src.users.application.service import UserService
from src.users.domain.schema import UserRepository as UserRepositoryInterface
from src.users.infra.db.mongodb.repositories.repository import UserRepositoryImpl


class InfrastructureProvider:
    async def get_user_repository(
        self,
        mongodb_repository: MongoDBRepositoryImpl = Depends(
            get_mongodb_repository_stub
        ),
    ) -> UserRepositoryInterface:
        return UserRepositoryImpl(mongodb_repository)

    async def get_mongodb_repository(self) -> MongoDBRepositoryImpl:
        return MongoDBRepositoryImpl(
            MongoDBClient(
                database_name="fluyo",
                connection_string="mongodb+srv://fluyo_mongo:Elpavorealverde-1@cluster0.53hl8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            )
        )

    async def get_user_service(
        self,
        user_repository: UserRepositoryInterface = Depends(get_user_repository_stub),
        session_token_repository: SessionTokenRepositoryImpl = Depends(
            get_session_token_repository_stub
        ),
    ) -> UserService:
        return UserService(user_repository, session_token_repository)

    async def get_session_token_repository(
        self,
        mongodb_repository: MongoDBRepositoryImpl = Depends(
            get_mongodb_repository_stub
        ),
    ) -> SessionTokenRepositoryImpl:
        return SessionTokenRepositoryImpl(mongodb_repository)

    async def get_company_repository(
        self,
        mongodb_repository: MongoDBRepositoryImpl = Depends(
            get_mongodb_repository_stub
        ),
    ) -> CompanyRepositoryImpl:
        return CompanyRepositoryImpl(mongodb_repository)

    async def get_company_service(
        self,
        company_repository: CompanyRepositoryImpl = Depends(
            get_company_repository_stub
        ),
        mongodb_repository: MongoDBRepositoryImpl = Depends(
            get_mongodb_repository_stub
        ),
    ) -> CompanyService:
        return CompanyService(company_repository, mongodb_repository)

    async def get_folder_storage_repository(self) -> FolderStorageRepository:
        return FolderStorageRepository(
            CloudStorageClient(
                bucket_name="fluyo_storage",
                project_id="fluyo-project-433921",
            )
        )

    async def get_folder_service(
        self,
        folder_storage_repository: FolderStorageRepository = Depends(
            get_folder_storage_repository_stub
        ),
        folder_repository: FolderRepositoryImpl = Depends(get_folder_repository_stub),
    ) -> FolderService:
        return FolderService(folder_storage_repository, folder_repository)

    async def get_folder_repository(
        self,
        mongodb_repository: MongoDBRepositoryImpl = Depends(
            get_mongodb_repository_stub
        ),
    ) -> FolderRepositoryImpl:
        return FolderRepositoryImpl(mongodb_repository)


async def auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_service: UserService = Depends(get_user_service_stub),
):
    try:
        return await user_service.get_user_info(credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
