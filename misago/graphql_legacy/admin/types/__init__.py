from ...pagetype import create_page_type
from .query import query_type
from .settings import settings_type
from .user import user_type

types = [
    create_page_type("UsersPage"),
    query_type,
    settings_type,
    user_type,
]
