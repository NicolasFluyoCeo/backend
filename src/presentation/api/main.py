import logfire
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.company.presentation.routes import company_router
from src.folder.presentation.routes import folder_router
from src.presentation.api.commons.exception_handlers import (
    generic_exception_handler,
    not_found_exception_handler,
    validation_error_exception_handler,
)
from src.presentation.api.di import setup_providers
from src.users.presentation.routes import user_router

LOGFIRE_TOKEN = "nl8p4kHkSvn7JXLNDRpwtfTCXGB6pzt42LKSDTrdK62S"


def create_app() -> FastAPI:
    app = FastAPI()
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(user_router)
    app.include_router(company_router)
    app.include_router(folder_router)
    setup_providers(app)
    app.add_exception_handler(Exception, handler=generic_exception_handler)
    app.add_exception_handler(
        status.HTTP_404_NOT_FOUND, handler=not_found_exception_handler
    )
    app.add_exception_handler(
        RequestValidationError, handler=validation_error_exception_handler
    )
    return app


logfire.configure(token=LOGFIRE_TOKEN)
app = create_app()
logfire.instrument_fastapi(app)
logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all"))
logfire.instrument_pymongo()
