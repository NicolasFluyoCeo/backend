from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.company.application.use_case.create_company.exceptions import (
    AdminUserNotFoundError,
    CompanyCreationError,
    DuplicateCompanyError,
    InvalidCompanyDataError,
    UnauthorizedCompanyCreationError,
)
from src.company.application.use_case.create_company.use_case import (
    CreateCompanyUseCase,
)
from src.company.domain.schema import CompanyDataInterface, CompanyInterface
from src.company.infra.db.dummy.repoitories.repository import DummyCompanyRepository
from src.core.infra.db.dummy.repository import DummyMongoDBRepository


@pytest.fixture
def company_repository():
    return DummyCompanyRepository()


@pytest.fixture
def mongodb_repository():
    return DummyMongoDBRepository()


@pytest.fixture
def use_case(company_repository, mongodb_repository):
    return CreateCompanyUseCase(company_repository, mongodb_repository)


@pytest.fixture
def valid_company_data():
    return CompanyDataInterface(
        name="Test Company",
        nit="123456789",
        address="Test Address",
        phone="1234567890",
        email="test@company.com",
    )


@pytest.mark.asyncio
async def test_create_company_success(use_case, valid_company_data, mongodb_repository):
    # Arrange
    admin_id = ObjectId()  # Crear el ObjectId primero
    admin_user_id = str(admin_id)
    await mongodb_repository.insert_one(
        "users",
        {"_id": admin_id},  # Usar el ObjectId directamente
    )

    # Act
    result = await use_case(valid_company_data, admin_user_id)

    # Assert
    assert isinstance(result, CompanyInterface)
    assert result.name == valid_company_data.name
    assert result.admin_user_id == admin_user_id


@pytest.mark.asyncio
async def test_create_company_duplicate_error(
    use_case, valid_company_data, mongodb_repository
):
    # Arrange
    admin_user_id = str(ObjectId())
    await mongodb_repository.insert_one("users", {"_id": ObjectId(admin_user_id)})
    await mongodb_repository.insert_one(
        "companies", {"name": valid_company_data.name, "admin_user_id": admin_user_id}
    )

    # Act & Assert
    with pytest.raises(DuplicateCompanyError):
        await use_case(valid_company_data, admin_user_id)


@pytest.mark.asyncio
async def test_create_company_admin_not_found(
    use_case, valid_company_data, mongodb_repository
):
    # Arrange
    admin_user_id = str(ObjectId())  # ID que no existe en la base de datos

    # Act & Assert
    with pytest.raises(AdminUserNotFoundError):
        await use_case(valid_company_data, admin_user_id)


@pytest.mark.asyncio
async def test_create_company_invalid_data(use_case, valid_company_data, mongodb_repository):
    # Arrange
    admin_id = ObjectId()
    admin_user_id = str(admin_id)
    await mongodb_repository.insert_one("users", {"_id": admin_id})
    
    # Simular validación fallida en el repositorio
    original_create = use_case._company_repository.create_company
    use_case._company_repository.create_company = AsyncMock(
        side_effect=InvalidCompanyDataError("Invalid company data")
    )

    try:
        # Act & Assert
        with pytest.raises(InvalidCompanyDataError):
            await use_case(valid_company_data, admin_user_id)
    finally:
        # Restaurar el método original
        use_case._company_repository.create_company = original_create


@pytest.mark.asyncio
async def test_create_company_unauthorized(
    use_case, valid_company_data, mongodb_repository
):
    # Arrange
    admin_id = ObjectId()
    admin_user_id = str(admin_id)
    await mongodb_repository.insert_one("users", {"_id": admin_id})
    
    # Simular error de autorización
    original_create = use_case._company_repository.create_company
    use_case._company_repository.create_company = AsyncMock(
        side_effect=UnauthorizedCompanyCreationError("Unauthorized attempt to create a company")
    )

    try:
        # Act & Assert
        with pytest.raises(UnauthorizedCompanyCreationError):
            await use_case(valid_company_data, admin_user_id)
    finally:
        # Restaurar el método original
        use_case._company_repository.create_company = original_create


@pytest.mark.asyncio
async def test_create_company_creation_error(
    use_case, valid_company_data, mongodb_repository
):
    # Arrange
    admin_id = ObjectId()
    admin_user_id = str(admin_id)
    await mongodb_repository.insert_one("users", {"_id": admin_id})

    # Modificar para simular un error en create_company
    original_create_company = use_case._company_repository.create_company
    use_case._company_repository.create_company = AsyncMock(
        side_effect=CompanyCreationError("Error creating company")
    )

    try:
        # Act & Assert
        with pytest.raises(CompanyCreationError):
            await use_case(valid_company_data, admin_user_id)
    finally:
        # Restaurar el método original
        use_case._company_repository.create_company = original_create_company
