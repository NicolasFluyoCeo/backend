from typing import Generic, TypeVar

from pydantic import BaseModel

DataType = TypeVar("DataType")


class BaseResponseModel(BaseModel, Generic[DataType]):
    error: bool
    message: str
    data: DataType
