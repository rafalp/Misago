from typing import Optional

from pydantic import BaseModel, HttpUrl
from pydantic.color import Color


class PluginManifest(BaseModel):
    name: str
    description: Optional[str]
    license: Optional[str]
    icon: Optional[str]
    color: Optional[Color]
    version: Optional[str]
    author: Optional[str]
    homepage: Optional[HttpUrl]
    repo: Optional[HttpUrl]
