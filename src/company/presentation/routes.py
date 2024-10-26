from fastapi import APIRouter, Depends

from src.company.application.service import CompanyService
from src.company.domain.schema import CompanyDataInterface
from src.presentation.api.di.stub import get_auth_user_stub, get_company_service_stub

company_router = APIRouter()


@company_router.post("/company")
async def create_company(
    company_data: CompanyDataInterface,
    company_service: CompanyService = Depends(get_company_service_stub),
    user_info=Depends(get_auth_user_stub),
):
    upload = await company_service.create_company(company_data, user_info.id)
    return {"company_id": upload.id}
