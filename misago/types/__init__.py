from datetime import datetime
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
from starlette.requests import Request

from ..errors import ErrorsList
from .category import Category
from .post import Post
from .thread import Thread
from .user import User


AsyncValidator = Callable[[Any, ErrorsList], Awaitable[Any]]

AuthenticateUserAction = Callable[
    ["GraphQLContext", str, str], Awaitable[Optional[User]]
]
AuthenticateUserFilter = Callable[
    [AuthenticateUserAction, "GraphQLContext", str, str], Awaitable[Optional[User]]
]

CacheVersions = Dict[str, str]


class CreateUserAction(Protocol):
    async def __call__(
        self,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> User:
        ...


class CreateUserFilter(Protocol):
    async def __call__(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> User:
        ...


CreateUserTokenAction = Callable[["GraphQLContext", User], Awaitable[str]]
CreateUserTokenFilter = Callable[
    [CreateUserTokenAction, "GraphQLContext", User], Awaitable[str]
]

CreateUserTokenPayloadAction = Callable[
    ["GraphQLContext", User], Awaitable[Dict[str, Any]]
]
CreateUserTokenPayloadFilter = Callable[
    [CreateUserTokenPayloadAction, "GraphQLContext", User], Awaitable[Dict[str, Any]],
]

GetAuthUserAction = Callable[["GraphQLContext", int], Awaitable[Optional[User]]]
GetAuthUserFilter = Callable[
    [GetAuthUserAction, "GraphQLContext", int], Awaitable[Optional[User]]
]

GetUserFromContextAction = Callable[["GraphQLContext"], Awaitable[Optional[User]]]
GetUserFromContextFilter = Callable[
    [GetUserFromContextAction, "GraphQLContext"], Awaitable[Optional[User]],
]

GetUserFromTokenAction = Callable[["GraphQLContext", str], Awaitable[Optional[User]]]
GetUserFromTokenFilter = Callable[
    [GetUserFromTokenAction, "GraphQLContext", str], Awaitable[Optional[User]],
]

GetUserFromTokenPayloadAction = Callable[
    ["GraphQLContext", Dict[str, Any]], Awaitable[Optional[User]]
]
GetUserFromTokenPayloadFilter = Callable[
    [GetUserFromTokenPayloadAction, "GraphQLContext", Dict[str, Any]],
    Awaitable[Optional[User]],
]

GraphQLContext = Dict[str, Any]
GraphQLContextAction = Callable[[Request], Awaitable[GraphQLContext]]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request], Awaitable[GraphQLContext]
]

PostThreadInput = Dict[str, Any]
PostThreadInputAction = Callable[
    ["GraphQLContext", Dict[str, List[AsyncValidator]], PostThreadInput, ErrorsList,],
    Awaitable[Tuple[PostThreadInput, ErrorsList]],
]
PostThreadInputFilter = Callable[
    [PostThreadInputAction, "GraphQLContext", PostThreadInput],
    Awaitable[Tuple[PostThreadInput, ErrorsList]],
]

PostThreadInputModel = Type[BaseModel]
PostThreadInputModelAction = Callable[
    ["GraphQLContext"], Awaitable[PostThreadInputModel]
]
PostThreadInputModelFilter = Callable[
    [PostThreadInputModelAction, "GraphQLContext"], Awaitable[PostThreadInputModel],
]

PostThreadAction = Callable[
    ["GraphQLContext", "PostThreadInput"], Awaitable[Tuple[Thread, Post]]
]
PostThreadFilter = Callable[
    [PostThreadAction, "GraphQLContext", "PostThreadInput"],
    Awaitable[Tuple[Thread, Post]],
]

RegisterInput = Dict[str, Any]
RegisterInputAction = Callable[
    ["GraphQLContext", Dict[str, List[AsyncValidator]], RegisterInput, ErrorsList,],
    Awaitable[Tuple[RegisterInput, ErrorsList]],
]
RegisterInputFilter = Callable[
    [RegisterInputAction, "GraphQLContext", RegisterInput],
    Awaitable[Tuple[RegisterInput, ErrorsList]],
]

RegisterInputModel = Type[BaseModel]
RegisterInputModelAction = Callable[["GraphQLContext"], Awaitable[RegisterInputModel]]
RegisterInputModelFilter = Callable[
    [RegisterInputModelAction, "GraphQLContext"], Awaitable[RegisterInputModel],
]

RegisterUserAction = Callable[["GraphQLContext", "RegisterInput"], Awaitable[User]]
RegisterUserFilter = Callable[
    [RegisterUserAction, "GraphQLContext", "RegisterInput"], Awaitable[User]
]


class SettingImage(TypedDict):
    path: str
    width: int
    height: int


Setting = Union[bool, int, str, List[str], SettingImage]
Settings = Dict[str, Setting]

TemplateContext = Dict[str, Any]
TemplateContextAction = Callable[[Request], Awaitable[TemplateContext]]
TemplateContextFilter = Callable[
    [TemplateContextAction, Request], Awaitable[TemplateContext]
]
