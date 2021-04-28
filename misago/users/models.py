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
    full_name: Optional[str]
    password: Optional[str]
    is_active: bool
    is_moderator: bool
    is_administrator: bool
    joined_at: datetime
    extra: dict
