from typing import List, Optional
from src.company.domain.protocols import CompanyRepository
from src.company.domain.schema import CompanyInterface


class DummyCompanyRepository(CompanyRepository):
    def __init__(self):
        self._companies: dict[str, CompanyInterface] = {}
        self._next_id = 1

    async def create_company(self, company: CompanyInterface) -> CompanyInterface:
        company_id = str(self._next_id)
        self._next_id += 1
        company.id = company_id
        self._companies[company_id] = company
        return company

    async def get_company_by_id(self, company_id: str) -> Optional[CompanyInterface]:
        return self._companies.get(company_id)

    async def get_company_by_nit(self, nit: str) -> Optional[CompanyInterface]:
        for company in self._companies.values():
            if company.nit == nit:
                return company
        return None

    async def update_company(self, company: CompanyInterface) -> CompanyInterface:
        if company.id not in self._companies:
            raise ValueError("Company not found")
        self._companies[company.id] = company
        return company

    async def delete_company(self, company_id: str) -> bool:
        if company_id not in self._companies:
            return False
        del self._companies[company_id]
        return True

    async def get_all_companies(self) -> List[CompanyInterface]:
        return list(self._companies.values())
