from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.presentation.api.commons.response_model import BaseResponseModel
from src.presentation.api.di.stub import get_auth_user_stub, get_user_service_stub
from src.users.application.service import UserService
from src.users.application.use_cases.login_user.exceptions import (
    IncorrectPasswordException,
    TokenGenerationException,
    UserNotFoundException,
)
from src.users.application.use_cases.register_user.exceptions import (
    EmailAlreadyExistsException,
    InvalidUserDataException,
    UserCreationException,
    WeakPasswordException,
)
from src.users.domain.schema import (
    UserDataInterface,
    UserLoginInterface,
    UserReadInterface,
)

user_router = APIRouter()


@user_router.post(
    "/users",
    responses={
        status.HTTP_201_CREATED: {"model": BaseResponseModel[UserReadInterface]},
        status.HTTP_400_BAD_REQUEST: {"model": BaseResponseModel[Dict]},
        status.HTTP_409_CONFLICT: {"model": BaseResponseModel[Dict]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseResponseModel[Dict]},
    },
)
async def create_user(
    user_data: UserDataInterface,
    user_service: UserService = Depends(get_user_service_stub),
):
    try:
        new_user = await user_service.register_user(user_data)
        return BaseResponseModel[UserReadInterface](
            error=False, message="User created successfully", data=new_user
        )
    except EmailAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidUserDataException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserCreationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except WeakPasswordException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": BaseResponseModel[str]},
        status.HTTP_400_BAD_REQUEST: {"model": BaseResponseModel[Dict]},
    },
)
async def login_user(
    user_data: UserLoginInterface,
    user_service: UserService = Depends(get_user_service_stub),
):
    try:
        token = await user_service.login_user(user_data)
        return BaseResponseModel[str](
            error=False, message="Login successful", data=token
        )
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except IncorrectPasswordException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except TokenGenerationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@user_router.get("/hello")
async def hello(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_info=Depends(get_auth_user_stub),
):
    try:
        return {"message": f"Hola, {user_info.username}!"}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
