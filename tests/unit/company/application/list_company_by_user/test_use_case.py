from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.company.application.use_case.list_company_by_user.use_case import (
    ListCompanyByUserUseCase,
)
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
    return ListCompanyByUserUseCase(company_repository, mongodb_repository)


@pytest.mark.asyncio
async def test_list_company_by_user_success(use_case, mongodb_repository):
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
    result = await use_case(user_id)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    company = result[0]
    assert company.id == company_id
    assert company.name == "Test Company"
    assert company.admin_user_id == user_id

    expected_query = {"$or": [{"admin_user_id": user_id}, {"users": user_id}]}
    mongodb_repository.find_many.assert_called_once_with("companies", expected_query)


@pytest.mark.asyncio
async def test_list_company_by_user_empty(use_case, mongodb_repository):
    # Arrange
    user_id = str(ObjectId())
    mongodb_repository.find_many = AsyncMock(return_value=[])

    # Act
    result = await use_case(user_id)

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0

    expected_query = {"$or": [{"admin_user_id": user_id}, {"users": user_id}]}
    mongodb_repository.find_many.assert_called_once_with("companies", expected_query)


@pytest.mark.asyncio
async def test_list_company_by_user_invalid_id(use_case, mongodb_repository):
    # Arrange
    invalid_user_id = "invalid_id"
    mongodb_repository.find_many = AsyncMock(side_effect=ValueError("Invalid ObjectId"))

    # Act & Assert
    with pytest.raises(ValueError):
        await use_case(invalid_user_id)


@pytest.mark.asyncio
async def test_list_company_by_user_repository_error(use_case, mongodb_repository):
    # Arrange
    user_id = str(ObjectId())
    mongodb_repository.find_many = AsyncMock(
        side_effect=Exception("Database connection error")
    )

    # Act & Assert
    with pytest.raises(Exception):
        await use_case(user_id)
