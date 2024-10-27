from src.company.application.use_case.create_company.exceptions import (
    AdminUserNotFoundError,
    CompanyCreationError,
    DuplicateCompanyError,
    InvalidCompanyDataError,
    UnauthorizedCompanyCreationError,
)
from src.company.domain.protocols import CompanyRepository
from src.company.domain.schema import CompanyDataInterface, CompanyInterface
from src.core.infra.db.mongodb.repository import MongoDBRepository


class CreateCompanyUseCase:
    def __init__(
        self,
        company_repository: CompanyRepository,
        mongodb_repository: MongoDBRepository,
    ):
        self._company_repository = company_repository
        self._mongodb_repository = mongodb_repository

    async def __call__(
        self, company_data: CompanyDataInterface, admin_user_id: str
    ) -> CompanyInterface:
        try:
            existing_company = await self._mongodb_repository.find_one(
                "companies",
                {"name": company_data.name, "admin_user_id": admin_user_id},
            )
            if existing_company:
                raise DuplicateCompanyError(
                    "A company with the same name and administrator already exists."
                )

            admin_user = await self._mongodb_repository.find_one(
                "users",
                {"_id": admin_user_id},
            )
            if not admin_user:
                raise AdminUserNotFoundError("The specified admin user was not found.")

            company_data_dict = company_data.model_dump()
            company_data_dict["admin_user_id"] = admin_user_id
            company_data_create = CompanyInterface(**company_data_dict)

            company = await self._company_repository.create_company(company_data_create)
            return company
        except InvalidCompanyDataError:
            raise InvalidCompanyDataError("The provided company data is invalid.")
        except UnauthorizedCompanyCreationError:
            raise UnauthorizedCompanyCreationError(
                "Unauthorized attempt to create a company."
            )
        except CompanyCreationError:
            raise CompanyCreationError("An error occurred while creating the company.")
