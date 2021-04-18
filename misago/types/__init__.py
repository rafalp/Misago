from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypedDict,
    Union,
)

from pydantic import BaseModel, PydanticTypeError, PydanticValueError

from ..errors import ErrorsList
from .category import Category
from .graphqlcontext import GraphQLContext
from .pagination import Pagination, PaginationPage
from .parsemarkup import ParsedMarkupMetadata
from .post import Post
from .richtext import RichText, RichTextBlock
from .settings import Setting, SettingImage, Settings
from .thread import Thread
from .threadpostspage import ThreadPostsPage
from .threadsfeed import ThreadsFeed
from .user import User
from .validator import Validator

CacheVersions = Dict[str, str]
