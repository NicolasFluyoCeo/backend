from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.company.application.service import CompanyService
from src.company.application.use_case.create_company.exceptions import (
    AdminUserNotFoundError,
    CompanyCreationError,
    DuplicateCompanyError,
    InvalidCompanyDataError,
    UnauthorizedCompanyCreationError,
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
def company_service(company_repository, mongodb_repository):
    return CompanyService(company_repository, mongodb_repository)


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
async def test_create_company_success(company_service, valid_company_data, mongodb_repository):
    # Arrange
    admin_id = ObjectId()
    admin_user_id = str(admin_id)
    await mongodb_repository.insert_one("users", {"_id": admin_id})

    # Act
    result = await company_service.create_company(valid_company_data, admin_user_id)

    # Assert
    assert isinstance(result, CompanyInterface)
    assert result.name == valid_company_data.name
    assert result.admin_user_id == admin_user_id


@pytest.mark.asyncio
async def test_create_company_duplicate_error(company_service, valid_company_data, mongodb_repository):
    # Arrange
    admin_user_id = str(ObjectId())
    await mongodb_repository.insert_one("users", {"_id": ObjectId(admin_user_id)})
    await mongodb_repository.insert_one(
        "companies", {"name": valid_company_data.name, "admin_user_id": admin_user_id}
    )

    # Act & Assert
    with pytest.raises(DuplicateCompanyError):
        await company_service.create_company(valid_company_data, admin_user_id)


@pytest.mark.asyncio
async def test_list_company_by_user_success(company_service, mongodb_repository):
    # Arrange
    user_id = str(ObjectId())
    company_id = str(ObjectId())
    expected_companies = [
        {
            "_id": ObjectId(company_id),
            "name": "Test Company",
            "nit": "123456789",
            "address": "Test Address",
            "phone": "1234567890",
            "email": "test@company.com",
            "admin_user_id": user_id,
            "users": [],
        }
    ]
    mongodb_repository.find_many = AsyncMock(return_value=expected_companies)

    # Act
    result = await company_service.list_company_by_user(user_id)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    company = result[0]
    assert company.id == company_id
    assert company.name == "Test Company"
    assert company.admin_user_id == user_id


@pytest.mark.asyncio
async def test_list_company_by_user_empty(company_service, mongodb_repository):
    # Arrange
    user_id = str(ObjectId())
    mongodb_repository.find_many = AsyncMock(return_value=[])

    # Act
    result = await company_service.list_company_by_user(user_id)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_company_info_success(company_service, mongodb_repository):
    # Arrange
    company_id = str(ObjectId())
    expected_company = CompanyInterface(
        id=company_id,
        name="Test Company",
        nit="123456789",
        address="Test Address",
        phone="1234567890",
        email="test@company.com",
        admin_user_id=str(ObjectId()),
        users=[]
    )
    company_service._company_repository.get_company_by_id = AsyncMock(return_value=expected_company)

    # Act
    result = await company_service.get_company_info(company_id)

    # Assert
    assert isinstance(result, CompanyInterface)
    assert result == expected_company


@pytest.mark.asyncio
async def test_get_company_info_not_found(company_service, mongodb_repository):
    # Arrange
    company_id = str(ObjectId())
    company_service._company_repository.get_company_by_id = AsyncMock(return_value=None)

    # Act & Assert
    result = await company_service.get_company_info(company_id)
    assert result is None

