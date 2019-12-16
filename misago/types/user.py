from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    slug: str
    email: str
    email_hash: str
    password: Optional[str]
    is_deactivated: bool
    is_moderator: bool
    is_admin: bool
    joined_at: datetime
    extra: dict
