from unittest.mock import AsyncMock

import pytest
from bson import ObjectId

from src.company.application.use_case.get_company_info.use_case import GetCompanyInfoUseCase
from src.company.domain.schema import CompanyInterface
from src.company.infra.db.dummy.repoitories.repository import DummyCompanyRepository


@pytest.fixture
def company_repository():
    return DummyCompanyRepository()


@pytest.fixture
def use_case(company_repository):
    return GetCompanyInfoUseCase(company_repository)


@pytest.mark.asyncio
async def test_get_company_info_success(use_case, company_repository):
    # Arrange
    company_id = str(ObjectId())
    expected_company = CompanyInterface(
        id=company_id,
        name="Test Company",
        nit="123456789",
        address="Test Address",
        phone="1234567890",
        email="test@company.com",
        admin_user_id=str(ObjectId())
    )
    company_repository.get_company_by_id = AsyncMock(return_value=expected_company)

    # Act
    result = await use_case(company_id)

    # Assert
    assert isinstance(result, CompanyInterface)
    assert result == expected_company
    company_repository.get_company_by_id.assert_called_once_with(company_id)


@pytest.mark.asyncio
async def test_get_company_info_not_found(use_case, company_repository):
    # Arrange
    company_id = str(ObjectId())
    company_repository.get_company_by_id = AsyncMock(return_value=None)

    # Act & Assert
    result = await use_case(company_id)
    assert result is None
    company_repository.get_company_by_id.assert_called_once_with(company_id)


@pytest.mark.asyncio 
async def test_get_company_info_invalid_id(use_case, company_repository):
    # Arrange
    invalid_company_id = "invalid_id"
    company_repository.get_company_by_id = AsyncMock(side_effect=ValueError("Invalid ObjectId"))

    # Act & Assert
    with pytest.raises(ValueError):
        await use_case(invalid_company_id)


@pytest.mark.asyncio
async def test_get_company_info_repository_error(use_case, company_repository):
    # Arrange
    company_id = str(ObjectId())
    company_repository.get_company_by_id = AsyncMock(
        side_effect=Exception("Database connection error")
    )

    # Act & Assert
    with pytest.raises(Exception):
        await use_case(company_id)
