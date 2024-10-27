from typing import List, Optional

from bson import ObjectId

from src.company.domain.protocols import CompanyRepository
from src.company.domain.schema import CompanyInterface
from src.core.infra.db.mongodb.repository import MongoDBRepository

# Add this new exception at the beginning of the file


class CompanyRepositoryImpl(CompanyRepository):
    def __init__(self, mongodb_repository: MongoDBRepository):
        self._mongodb_repository = mongodb_repository
        self._collection = "companies"

    async def create_company(self, company: CompanyInterface) -> CompanyInterface:
        company_dict = company.model_dump(exclude={"id"}, by_alias=True)
        result = await self._mongodb_repository.insert_one(
            self._collection, company_dict
        )
        return CompanyInterface.model_validate({"_id": str(result.inserted_id), **company_dict})

    async def get_company_by_id(self, company_id: str) -> Optional[CompanyInterface]:
        company = await self._mongodb_repository.find_one(
            self._collection, {"_id": ObjectId(company_id)}
        )
        if company:
            company['id'] = str(company['_id'])
            company['_id'] = str(company['_id'])
            return CompanyInterface(**company)
        return None

    async def get_company_by_nit(self, nit: str) -> Optional[CompanyInterface]:
        company = await self._mongodb_repository.find_one(
            self._collection, {"nit": nit}
        )
        return CompanyInterface(**company) if company else None

    async def update_company(self, company: CompanyInterface) -> CompanyInterface:
        await self._mongodb_repository.update_one(
            self._collection, {"_id": ObjectId(company.id)}, company.model_dump()
        )
        return company

    async def delete_company(self, company_id: str) -> bool:
        result = await self._mongodb_repository.delete_one(
            self._collection, {"_id": ObjectId(company_id)}
        )
        return result.deleted_count == 1

    async def get_all_companies(self) -> List[CompanyInterface]:
        companies = await self._mongodb_repository.find_many(self._collection)
        return [CompanyInterface(**company) for company in companies]

    def _create_company_interface(self, company_data: dict) -> CompanyInterface:
        company_data_copy = company_data.copy()
        company_id = str(company_data_copy.pop("_id"))
        # Make sure 'id' is not in company_data_copy
        company_data_copy.pop("id", None)
        return CompanyInterface(id=company_id, **company_data_copy)
