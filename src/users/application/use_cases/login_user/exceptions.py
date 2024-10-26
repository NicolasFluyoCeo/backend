from typing import Optional

from src.users.application.use_cases.exceptions import UserBaseException


class UserNotFoundException(UserBaseException):
    """
    Exception raised when a user is not found.
    """

    def __init__(self, email: Optional[str] = None, *args):
        super().__init__(args)
        self.email = email

    def __str__(self) -> str:
        return f"User not found: {self.email}" if self.email else "User not found"


class IncorrectPasswordException(UserBaseException):
    """
    Exception raised when the provided password is incorrect.
    """

    def __str__(self) -> str:
        return "Incorrect password"


class TokenGenerationException(UserBaseException):
    """
    Exception raised when there's an error generating the token.
    """

    def __init__(self, message: str, *args):
        super().__init__(args)
        self.message = message

    def __str__(self) -> str:
        return f"Error generating token: {self.message}"
