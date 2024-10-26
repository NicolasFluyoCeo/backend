from fastapi import Depends

from src.company.application.service import CompanyService
from src.company.infra.db.mongodb.repoitories.repository import CompanyRepositoryImpl
from src.core.infra.db.mongodb.client import Client as MongoDBClient
from src.core.infra.db.mongodb.repository import (
    MongoDBRepositoryImpl,
    SessionTokenRepositoryImpl,
)
from src.presentation.api.di.stub import (
    get_company_repository_stub,
    get_mongodb_repository_stub,
    get_session_token_repository_stub,
    get_user_repository_stub,
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
    ) -> CompanyService:
        return CompanyService(company_repository)
