from src.company.domain.schema import CompanyInterface
from src.company.infra.db.mongodb.repoitories.repository import CompanyRepository


class GetCompanyInfoUseCase:
    def __init__(self, company_repository: CompanyRepository):
        self._company_repository = company_repository

    async def __call__(self, company_id: str) -> CompanyInterface:
        return await self._company_repository.get_company_by_id(company_id)
