from fastapi import APIRouter, Depends, File, UploadFile

from src.folder.application.service import FolderService
from src.folder.domain.schema import FileNameDescriptionUrl, Folder
from src.presentation.api.di.stub import get_folder_service_stub

folder_router = APIRouter()


@folder_router.post("/upload-folder")
async def upload_folder(
    company_id: str,
    file: UploadFile = File(...),
    folder_service: FolderService = Depends(get_folder_service_stub),
):
    content = await file.read()
    file_info = FileNameDescriptionUrl(
        name=file.filename,
        description="",  # Puedes agregar una descripción si es necesario
    )
    folder = Folder(
        file=file_info,
        description="",  # Puedes agregar una descripción si es necesario
    )
    await folder_service.upload_folder(company_id, folder, content, file.content_type)
    return {"message": "Folder uploaded successfully"}


@folder_router.get("/list-folders")
async def list_folders(
    company_id: str, folder_service: FolderService = Depends(get_folder_service_stub)
):
    return await folder_service.list_folders(company_id)
