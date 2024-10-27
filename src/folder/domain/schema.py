from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class FolderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    COMPLETED = "completed"
    FAILED = "failed"
    PROGRESS = "progress"


class File(BaseModel):
    name: str
    content: bytes
    mimetype: str


class FileNameDescriptionUrl(BaseModel):
    name: str
    description: str
    path: Optional[str] = None


class Folder(BaseModel):
    file: Optional[FileNameDescriptionUrl] = None
    description: str


class FolderRepositorySchema(BaseModel):
    _id: Optional[str] = None
    company_id: str
    name: str
    description: str
    path: Optional[str] = None
    status: FolderStatus = FolderStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    overview: Optional[str] = None
