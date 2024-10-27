from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from src.folder.application.service import FolderService
from src.folder.domain.schema import FileNameDescriptionUrl, Folder
from src.presentation.api.di.stub import get_folder_service_stub
from src.presentation.api.commons.response_model import BaseResponseModel

folder_router = APIRouter(tags=["folders"])


@folder_router.post(
    "/upload-folder",
    responses={
        status.HTTP_201_CREATED: {"model": BaseResponseModel[dict]},
        status.HTTP_400_BAD_REQUEST: {"model": BaseResponseModel[dict]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseResponseModel[dict]},
    },
)
async def upload_folder(
    company_id: str,
    file: UploadFile = File(...),
    folder_service: FolderService = Depends(get_folder_service_stub),
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    try:
        content = await file.read()
        file_info = FileNameDescriptionUrl(
            name=file.filename,
            description="",  # You can add a description if needed
        )
        folder = Folder(
            file=file_info,
            description="",  # You can add a description if needed
        )
        await folder_service.upload_folder(company_id, folder, content, file.content_type)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=BaseResponseModel(
                error=False,
                message="Folder uploaded successfully",
                data={"company_id": company_id, "filename": file.filename},
            ).model_dump()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading folder: {str(e)}"
        )


@folder_router.get(
    "/list-folders",
    responses={
        status.HTTP_200_OK: {"model": BaseResponseModel[list]},
        status.HTTP_404_NOT_FOUND: {"model": BaseResponseModel[dict]},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BaseResponseModel[dict]},
    },
)
async def list_folders(
    company_id: str, folder_service: FolderService = Depends(get_folder_service_stub)
):
    try:
        folders = await folder_service.list_folders(company_id)
        if not folders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No folders found for this company"
            )
        return BaseResponseModel(
            error=False,
            message="Folders retrieved successfully",
            data=folders,
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing folders: {str(e)}"
        )


@folder_router.get(
    "/get-folder",
)
async def get_folder(
    company_id: str, folder_id: str, folder_service: FolderService = Depends(get_folder_service_stub)
):
    folder = await folder_service.get_folder(company_id, folder_id)
    return BaseResponseModel(
        error=False,
        message="Folder retrieved successfully",
        data=folder,
    )
