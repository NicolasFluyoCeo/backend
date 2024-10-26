from typing import Optional

from pydantic import AnyUrl, BaseModel


class File(BaseModel):
    name: str
    content: bytes
    mimetype: str


class FileNameDescriptionUrl(BaseModel):
    name: str
    description: str
    url: Optional[AnyUrl] = None


class Folder(BaseModel):
    file: Optional[FileNameDescriptionUrl] = None
    description: str
