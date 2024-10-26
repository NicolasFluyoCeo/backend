from fastapi import APIRouter, Depends, File, UploadFile

from src.folder.application.service import FolderService
from src.folder.domain.schema import File as FileSchema
from src.folder.domain.schema import Folder
from src.presentation.api.di.stub import get_folder_service_stub

folder_router = APIRouter()


@folder_router.post("/upload-folder")
async def upload_folder(
    company_id: str,
    file: UploadFile = File(...),
    folder_service: FolderService = Depends(get_folder_service_stub),
):
    content = await file.read()
    folder = Folder(
        file=FileSchema(
            name=file.filename, content=content, mimetype=file.content_type
        ),
        description="",  # Puedes agregar una descripción si es necesario
    )
    await folder_service.upload_folder(company_id, folder)
    return {"message": "Folder uploaded successfully"}
