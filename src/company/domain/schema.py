from typing import Any, List, Optional

from pydantic import BaseModel, Field


class CompanyInterface(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    nit: str
    address: str
    phone: str
    email: str
    admin_user_id: str
    users: Optional[List[str]] = []

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    @classmethod
    def model_validate(cls, obj: Any) -> "CompanyInterface":
        if isinstance(obj, dict):
            obj = obj.copy()
            if "_id" in obj:
                obj["id"] = str(obj["_id"])
                obj["_id"] = str(obj["_id"])
        return super().model_validate(obj)


class CompanyDataInterface(BaseModel):
    name: str
    nit: str
    address: str
    phone: str
    email: str
