from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MisagoPlugin:
    name: Optional[str] = None
    description: Optional[str] = None
    license: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    homepage: Optional[str] = None
    sponsor: Optional[str] = None
    help: Optional[str] = None
    bugs: Optional[str] = None
    repo: Optional[str] = None
