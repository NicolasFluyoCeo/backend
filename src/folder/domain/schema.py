from typing import Optional

from pydantic import BaseModel


class File(BaseModel):
    name: str
    content: bytes
    mimetype: str


class Folder(BaseModel):
    file: Optional[File] = None
    description: str
