from datetime import datetime, timezone

import jwt

from src.core.infra.db.mongodb.repository import SessionTokenRepositoryImpl
from src.users.application.use_cases.user_info.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    TokenNotFoundException,
    TokenRevokedException,
    UserNotFoundException,
)
from src.users.domain.schema import UserReadInterface, UserRepository


class GetUserInfoUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        session_token_repository: SessionTokenRepositoryImpl,
        secret_key: str,
    ):
        self.user_repository = user_repository
        self.session_token_repository = session_token_repository
        self.secret_key = secret_key

    async def __call__(self, token: str) -> UserReadInterface:
        try:
            # First, decode the token to validate JWT exceptions
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenException("Invalid token")

        # Validate that the token exists in the database and has not been revoked
        session = await self.session_token_repository.get_jwt_token(token)
        print(session)
        if not session:
            raise TokenNotFoundException("There is an invalid token")
        if session.get("revoked"):
            raise TokenRevokedException("Token has been revoked")

        # Verify token expiration (although JWT already does this, we keep it just in case)
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
            timezone.utc
        ):
            raise TokenExpiredException("Token has expired")

        # Get user information
        user_id = payload.get("user_id")
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")

        return UserReadInterface(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            cell_phone=user.cell_phone,
        )
