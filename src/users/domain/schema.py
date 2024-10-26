from datetime import datetime
from enum import Enum
from typing import List, Optional, Protocol

from pydantic import BaseModel, EmailStr, SecretStr


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class UserLoginInterface(BaseModel):
    email: EmailStr
    password: SecretStr

    def get_password_bytes(self) -> bytes:
        return self.password.get_secret_value().encode("utf-8")


class UserReadInterface(BaseModel):
    id: str
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    cell_phone: str


class UserInterface(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: SecretStr
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    cell_phone: str

    def get_password_bytes(self) -> bytes:
        return self.password.get_secret_value().encode("utf-8")


class UserDataInterface(BaseModel):
    """
    Protocol defining the interface for user data.
    This interface specifies the structure of the data used for creating a user.
    """

    username: str
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: UserRole = UserRole.ADMIN
    cell_phone: Optional[str]


class UserCreator(Protocol):
    """
    Protocol defining the interface for creating a user in the database.
    This interface specifies the method that must be implemented to create a new user.
    """

    def create_user(self, user_data: UserDataInterface) -> UserInterface:
        """
        Creates a new user in the database.

        Args:
            user_data (UserDataInterface): An object containing the user's information.

        Returns:
            UserInterface: The created user object implementing the UserInterface.

        Raises:
            ValueError: If required fields are missing or if the username or email already exists.
        """
        ...


class UserRepository(Protocol):
    """
    Protocol defining the interface for a user repository.
    This interface specifies the methods that must be implemented to perform CRUD operations on users.
    """

    async def get_user_by_email(self, email: EmailStr) -> Optional[UserInterface]:
        """
        Retrieves a user by their email address.
        """
        ...

    async def create_user(self, user_data: UserDataInterface) -> UserInterface:
        """
        Creates a new user in the database.

        Args:
            user_data (UserDataInterface): The data for the new user.

        Returns:
            UserInterface: The created user.
        """
        ...

    async def get_user_by_id(self, user_id: str) -> Optional[UserInterface]:
        """
        Retrieves a user by their ID.

        Args:
            user_id (str): The ID of the user to search for.

        Returns:
            Optional[UserInterface]: The found user or None if it doesn't exist.
        """
        ...

    async def update_user(self, user: UserInterface) -> UserInterface:
        """
        Updates the information of an existing user.

        Args:
            user (UserInterface): The user object with updated information.

        Returns:
            UserInterface: The updated user.
        """
        ...

    async def delete_user(self, user_id: str) -> bool:
        """
        Deletes a user from the database.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        ...

    async def get_all_users(self) -> List[UserInterface]:
        """
        Retrieves all users from the database.

        Returns:
            List[UserInterface]: A list of all users.
        """
        ...
