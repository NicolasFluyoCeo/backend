from typing import Optional

from pydantic import BaseModel


class CompanyInterface(BaseModel):
    id: Optional[str] = None
    name: str
    nit: str
    address: str
    phone: str
    email: str
    admin_user_id: str


class CompanyDataInterface(BaseModel):
    name: str
    nit: str
    address: str
    phone: str
    email: str
