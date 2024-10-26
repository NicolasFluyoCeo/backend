from src.core.infra.db.mongodb.repository import SessionTokenRepositoryImpl
from src.users.application.use_cases.login_user.use_case import LoginUserUseCase
from src.users.application.use_cases.register_user.use_case import RegisterUserUseCase
from src.users.application.use_cases.user_info.use_case import GetUserInfoUseCase
from src.users.domain.schema import (
    UserDataInterface,
    UserLoginInterface,
    UserReadInterface,
    UserRepository,
)


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        session_token_repository: SessionTokenRepositoryImpl,
    ):
        self.user_repository = user_repository
        self.session_token_repository = session_token_repository

    async def register_user(self, user_data: UserDataInterface) -> UserReadInterface:
        use_case = RegisterUserUseCase(self.user_repository)
        return await use_case(user_data)

    async def login_user(self, user_data: UserLoginInterface) -> str:
        use_case = LoginUserUseCase(
            self.user_repository, "SECRET_KEY", self.session_token_repository
        )
        return await use_case(user_data)
    
    async def get_user_info(self, token: str) -> UserReadInterface:
        use_case = GetUserInfoUseCase(
            self.user_repository, self.session_token_repository, "SECRET_KEY"
        )
        return await use_case(token)
