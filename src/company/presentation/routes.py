from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.company.application.service import CompanyService
from src.company.application.use_case.create_company.exceptions import (
    AdminUserNotFoundError,
    CompanyCreationError,
    DuplicateCompanyError,
    InvalidCompanyDataError,
    UnauthorizedCompanyCreationError,
)
from src.company.domain.schema import CompanyDataInterface
from src.presentation.api.commons.response_model import BaseResponseModel
from src.presentation.api.di.stub import get_auth_user_stub, get_company_service_stub

company_router = APIRouter(tags=["company"], prefix="/company")


@company_router.post("", response_model=BaseResponseModel[Dict[str, Any]])
async def create_company(
    company_data: CompanyDataInterface,
    company_service: CompanyService = Depends(get_company_service_stub),
    user_info=Depends(get_auth_user_stub),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    try:
        company = await company_service.create_company(company_data, user_info.id)
        company_data = company.model_dump()
        return BaseResponseModel(
            error=False,
            message="Company created successfully",
            data=company_data,
        )
    except InvalidCompanyDataError:
        raise HTTPException(status_code=400, detail="Invalid company data")
    except UnauthorizedCompanyCreationError:
        raise HTTPException(
            status_code=403, detail="Not authorized to create a company"
        )
    except DuplicateCompanyError:
        raise HTTPException(status_code=409, detail="Company already exists")
    except AdminUserNotFoundError:
        raise HTTPException(status_code=404, detail="Admin user not found")
    except CompanyCreationError:
        raise HTTPException(status_code=500, detail="Error creating the company")


@company_router.get("", response_model=BaseResponseModel[List[Dict[str, Any]]])
async def list_company_by_user(
    company_service: CompanyService = Depends(get_company_service_stub),
    user_info=Depends(get_auth_user_stub),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    companies = await company_service.list_company_by_user(user_info.id)
    companies_data = [company.model_dump() for company in companies]
    return BaseResponseModel(
        error=False, message="Empresas listadas exitosamente", data=companies_data
    )


@company_router.get(
    "/{company_id}", response_model=BaseResponseModel[Dict[str, Any]]
)
async def get_company_info(
    company_id: str,
    company_service: CompanyService = Depends(get_company_service_stub),
    user_info=Depends(get_auth_user_stub),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    try:
        # Check if the user belongs to the company
        companies = await company_service.list_company_by_user(user_info.id)
        if not any(company.id == company_id for company in companies):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to view this company's information",
            )

        company = await company_service.get_company_info(company_id)
        return BaseResponseModel(
            error=False,
            message="Company information retrieved successfully",
            data=company.model_dump(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving company information: {str(e)}"
        )
