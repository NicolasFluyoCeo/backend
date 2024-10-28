import pytest
from unittest.mock import Mock, AsyncMock
from bson import ObjectId

from src.company.domain.schema import CompanyInterface
from src.company.infra.db.mongodb.repoitories.repository import CompanyRepositoryImpl
from src.core.infra.db.mongodb.repository import MongoDBRepository

@pytest.fixture
def mongodb_repository():
    return Mock(spec=MongoDBRepository)

@pytest.fixture
def company_repository(mongodb_repository):
    return CompanyRepositoryImpl(mongodb_repository)

@pytest.fixture
def sample_company():
    return CompanyInterface(
        id="507f1f77bcf86cd799439011",
        name="Test Company",
        nit="123456789",
        address="Test Address",
        phone="1234567890",
        email="test@company.com",  # Campo requerido añadido
        admin_user_id="507f1f77bcf86cd799439012"  # Campo requerido añadido
    )

@pytest.mark.asyncio
async def test_create_company(company_repository, mongodb_repository, sample_company):
    # Arrange
    mongodb_repository.insert_one = AsyncMock(return_value=Mock(inserted_id=ObjectId(sample_company.id)))
    
    # Act
    result = await company_repository.create_company(sample_company)
    
    # Assert
    assert isinstance(result, CompanyInterface)
    assert result.id == sample_company.id
    mongodb_repository.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_company_by_id(company_repository, mongodb_repository, sample_company):
    # Arrange
    company_dict = sample_company.model_dump()
    company_dict["_id"] = ObjectId(sample_company.id)
    mongodb_repository.find_one = AsyncMock(return_value=company_dict)
    
    # Act
    result = await company_repository.get_company_by_id(sample_company.id)
    
    # Assert
    assert isinstance(result, CompanyInterface)
    assert result.id == sample_company.id
    mongodb_repository.find_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_company_by_id_not_found(company_repository, mongodb_repository):
    # Arrange
    mongodb_repository.find_one = AsyncMock(return_value=None)
    
    # Act
    result = await company_repository.get_company_by_id("507f1f77bcf86cd799439011")
    
    # Assert
    assert result is None
    mongodb_repository.find_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_company_by_nit(company_repository, mongodb_repository, sample_company):
    # Arrange
    company_dict = sample_company.model_dump()
    mongodb_repository.find_one = AsyncMock(return_value=company_dict)
    
    # Act
    result = await company_repository.get_company_by_nit(sample_company.nit)
    
    # Assert
    assert isinstance(result, CompanyInterface)
    assert result.nit == sample_company.nit
    mongodb_repository.find_one.assert_called_once()

@pytest.mark.asyncio
async def test_update_company(company_repository, mongodb_repository, sample_company):
    # Arrange
    mongodb_repository.update_one = AsyncMock()
    
    # Act
    result = await company_repository.update_company(sample_company)
    
    # Assert
    assert isinstance(result, CompanyInterface)
    assert result.id == sample_company.id
    mongodb_repository.update_one.assert_called_once()

@pytest.mark.asyncio
async def test_delete_company(company_repository, mongodb_repository):
    # Arrange
    mongodb_repository.delete_one = AsyncMock(return_value=Mock(deleted_count=1))
    
    # Act
    result = await company_repository.delete_company("507f1f77bcf86cd799439011")
    
    # Assert
    assert result is True
    mongodb_repository.delete_one.assert_called_once()

@pytest.mark.asyncio
async def test_delete_company_not_found(company_repository, mongodb_repository):
    # Arrange
    mongodb_repository.delete_one = AsyncMock(return_value=Mock(deleted_count=0))
    
    # Act
    result = await company_repository.delete_company("507f1f77bcf86cd799439011")
    
    # Assert
    assert result is False
    mongodb_repository.delete_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_companies(company_repository, mongodb_repository, sample_company):
    # Arrange
    companies = [sample_company.model_dump()]
    mongodb_repository.find_many = AsyncMock(return_value=companies)
    
    # Act
    result = await company_repository.get_all_companies()
    
    # Assert
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], CompanyInterface)
    mongodb_repository.find_many.assert_called_once()
