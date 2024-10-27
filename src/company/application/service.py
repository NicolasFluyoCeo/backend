from typing import List

from src.company.application.use_case.create_company.use_case import (
    CreateCompanyUseCase,
)
from src.company.application.use_case.list_company_by_user.use_case import (
    ListCompanyByUserUseCase,
)
from src.company.domain.protocols import CompanyRepository
from src.company.domain.schema import CompanyDataInterface, CompanyInterface
from src.core.infra.db.mongodb.repository import MongoDBRepository


class CompanyService:
    def __init__(
        self,
        company_repository: CompanyRepository,
        mongodb_repository: MongoDBRepository,
    ):
        self._company_repository = company_repository
        self._mongodb_repository = mongodb_repository

    async def create_company(
        self, company_data: CompanyDataInterface, admin_user_id: str
    ) -> CompanyInterface:
        create_company_use_case = CreateCompanyUseCase(
            self._company_repository, self._mongodb_repository
        )
        return await create_company_use_case(company_data, admin_user_id)

    async def list_company_by_user(self, user_id: str) -> List[CompanyInterface]:
        list_company_by_user_use_case = ListCompanyByUserUseCase(
            self._company_repository, self._mongodb_repository
        )
        return await list_company_by_user_use_case(user_id)
