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
        # Validar que el token es válido, existe en la base de datos y no ha sido revocado
        session = await self.session_token_repository.get_jwt_token(token)
        if not session:
            raise TokenNotFoundException("Token no encontrado en la base de datos")
        if session.get("revoked"):
            raise TokenRevokedException("El token ha sido revocado")

        try:
            # Decodificar el token
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])

            # Verificar la expiración del token
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
                timezone.utc
            ):
                raise TokenExpiredException("El token ha expirado")

            # Obtener información del usuario
            user_id = payload.get("user_id")
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise UserNotFoundException(f"Usuario con ID {user_id} no encontrado")

            return UserReadInterface(
                id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                cell_phone=user.cell_phone,
            )

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException("El token ha expirado")
        except jwt.InvalidTokenError:
            raise InvalidTokenException("Token inválido")
