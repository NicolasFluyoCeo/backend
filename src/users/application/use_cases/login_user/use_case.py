from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from pydantic import SecretStr

from src.core.infra.db.mongodb.repository import SessionTokenRepositoryImpl
from src.users.application.use_cases.login_user.exceptions import (
    IncorrectPasswordException,
    TokenGenerationException,
    UserNotFoundException,
)
from src.users.domain.schema import (
    UserLoginInterface,
    UserReadInterface,
    UserRepository,
)


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        secret_key: str,
        session_token_repository: SessionTokenRepositoryImpl,
    ):
        self.user_repository = user_repository
        self.secret_key = secret_key
        self.session_token_repository = session_token_repository

    async def __call__(self, user_data: UserLoginInterface) -> str:
        user = await self.user_repository.get_user_by_email(user_data.email)
        if not user:
            raise UserNotFoundException(user_data.email)

        if not self._verify_password(user.password, user_data.password):
            raise IncorrectPasswordException()

        try:
            token = self._generate_token(user)
            await self.session_token_repository.create_session(
                {"token": token, "user_id": user.id}
            )
            return token
        except Exception as e:
            raise TokenGenerationException(str(e))

    def _verify_password(
        self, stored_password: SecretStr, input_password: SecretStr
    ) -> bool:
        return bcrypt.checkpw(
            input_password.get_secret_value().encode("utf-8"),
            stored_password.get_secret_value().encode("utf-8"),
        )

    def _generate_token(self, user: UserReadInterface) -> str:
        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
