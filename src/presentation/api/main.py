from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError

from src.company.presentation.routes import company_router
from src.presentation.api.commons.exception_handlers import (
    generic_exception_handler,
    not_found_exception_handler,
    validation_error_exception_handler,
)
from src.presentation.api.di import setup_providers
from src.users.presentation.routes import user_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(company_router)
    setup_providers(app)
    app.add_exception_handler(Exception, handler=generic_exception_handler)
    app.add_exception_handler(
        status.HTTP_404_NOT_FOUND, handler=not_found_exception_handler
    )
    app.add_exception_handler(
        RequestValidationError, handler=validation_error_exception_handler
    )
    return app


app = create_app()
