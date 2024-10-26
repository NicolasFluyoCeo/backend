from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.company.application.service import CompanyService
from src.company.domain.schema import CompanyDataInterface
from src.presentation.api.di.stub import get_company_service_stub, get_user_service_stub
from src.users.application.service import UserService

company_router = APIRouter()


@company_router.post("/company")
async def create_company(
    company_data: CompanyDataInterface,
    company_service: CompanyService = Depends(get_company_service_stub),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    user_service: UserService = Depends(get_user_service_stub),
):
    user_info = await user_service.get_user_info(credentials.credentials)
    return await company_service.create_company(company_data, user_info.id)
