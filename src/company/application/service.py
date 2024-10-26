from src.company.domain.protocols import CompanyRepository
from src.company.domain.schema import CompanyDataInterface, CompanyInterface


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository

    async def create_company(
        self, company_data: CompanyDataInterface, admin_user_id: str
    ) -> CompanyInterface:
        company_data_create = CompanyInterface(
            **company_data.model_dump(), admin_user_id=admin_user_id
        )
        return await self._company_repository.create_company(company_data_create)
