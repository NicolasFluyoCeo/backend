from typing import List

from src.company.domain.protocols import CompanyRepository
from src.company.domain.schema import CompanyInterface
from src.core.infra.db.mongodb.repository import MongoDBRepository


class ListCompanyByUserUseCase:
    def __init__(
        self,
        company_repository: CompanyRepository,
        mongodb_repository: MongoDBRepository,
    ):
        self._company_repository = company_repository
        self._mongodb_repository = mongodb_repository

    async def __call__(self, user_id: str) -> List[CompanyInterface]:
        query = {"$or": [{"admin_user_id": user_id}, {"users": user_id}]}
        companies = await self._mongodb_repository.find_many("companies", query)
        data = [
            CompanyInterface.model_validate(
                {**company, "id": str(company["_id"]), "_id": str(company["_id"])}
            )
            for company in companies
        ]
        return data
