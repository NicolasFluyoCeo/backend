import re

import bcrypt

from src.users.application.use_cases.register_user.exceptions import (
    EmailAlreadyExistsException,
    InvalidUserDataException,
    UserCreationException,
    WeakPasswordException,
)
from src.users.domain.schema import UserDataInterface, UserReadInterface, UserRepository


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_data: UserDataInterface) -> UserReadInterface:
        try:
            existing_user = await self.user_repository.get_user_by_email(
                user_data.email
            )
            if existing_user:
                raise EmailAlreadyExistsException(user_data.email)

            # Validate and hash the password
            if not self._is_password_strong(user_data.password):
                raise WeakPasswordException(
                    "The password does not meet the security requirements."
                )

            hashed_password = self._hash_password(user_data.password)

            # Create the user with the hashed password
            new_user = await self.user_repository.create_user(
                UserDataInterface(
                    **user_data.model_dump(exclude={"password"}),
                    password=hashed_password,
                )
            )
            return new_user
        except ValueError as e:
            raise InvalidUserDataException(str(e))
        except Exception as e:
            raise UserCreationException(str(e))

    def _is_password_strong(self, password: str) -> bool:
        return (
            len(password) >= 8
            and re.search(r"\d", password)
            and re.search(r"[A-Z]", password)
        )

    def _hash_password(self, password: str) -> str:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
