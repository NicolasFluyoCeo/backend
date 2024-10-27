from fastapi import FastAPI

from src.presentation.api.di.providers import InfrastructureProvider, auth_user
from src.presentation.api.di.stub import (
    get_auth_user_stub,
    get_company_repository_stub,
    get_company_service_stub,
    get_folder_repository_stub,
    get_folder_service_stub,
    get_folder_storage_repository_stub,
    get_mongodb_repository_stub,
    get_session_token_repository_stub,
    get_user_repository_stub,
    get_user_service_stub,
)

infrastructure_provider = InfrastructureProvider()


def setup_providers(app: FastAPI):
    app.dependency_overrides[get_mongodb_repository_stub] = (
        infrastructure_provider.get_mongodb_repository
    )
    app.dependency_overrides[get_user_repository_stub] = (
        infrastructure_provider.get_user_repository
    )
    app.dependency_overrides[get_user_service_stub] = (
        infrastructure_provider.get_user_service
    )
    app.dependency_overrides[get_session_token_repository_stub] = (
        infrastructure_provider.get_session_token_repository
    )
    app.dependency_overrides[get_company_repository_stub] = (
        infrastructure_provider.get_company_repository
    )
    app.dependency_overrides[get_company_service_stub] = (
        infrastructure_provider.get_company_service
    )
    app.dependency_overrides[get_auth_user_stub] = auth_user
    app.dependency_overrides[get_folder_storage_repository_stub] = (
        infrastructure_provider.get_folder_storage_repository
    )
    app.dependency_overrides[get_folder_service_stub] = (
        infrastructure_provider.get_folder_service
    )
    app.dependency_overrides[get_folder_repository_stub] = (
        infrastructure_provider.get_folder_repository
    )
