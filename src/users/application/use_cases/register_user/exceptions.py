from typing import Optional

from pydantic import EmailStr

from src.users.application.use_cases.exceptions import UserBaseException


class RegisterUserException(UserBaseException):
    """Base exception for the Register User use case"""


class EmailAlreadyExistsException(RegisterUserException):
    """
    Exception raised when the email is already registered.
    """

    def __init__(self, email: EmailStr, *args):
        super().__init__(args)
        self.email = email

    def __str__(self) -> str:
        return f"The email {self.email} is already registered"


class InvalidUserDataException(RegisterUserException):
    """
    Exception raised when the user data is invalid.
    """

    def __init__(self, field: Optional[str] = None, *args):
        super().__init__(args)
        self.field = field

    def __str__(self) -> str:
        return f"Invalid user data: {self.field}"


class UserCreationException(RegisterUserException):
    """
    Exception raised when there's an error creating the user in the database.
    """

    def __init__(self, error_message: Optional[str] = None, *args):
        super().__init__(args)
        self.error_message = error_message

    def __str__(self) -> str:
        return f"Error creating user: {self.error_message}"


class WeakPasswordException(RegisterUserException):
    """
    Exception raised when the password does not meet the security requirements.
    """

    def __init__(self, error_message: str, *args):
        super().__init__(args)
        self.error_message = error_message

    def __str__(self) -> str:
        return f"Weak password: {self.error_message}"
