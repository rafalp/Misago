from datetime import datetime
from typing import (
    Any,
    Callable,
    Coroutine,
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


AsyncRootValidator = Callable[[Any, Any], Coroutine[Any, Any, None]]
AsyncValidator = Callable[[Any], Coroutine[Any, Any, None]]

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
    ) -> "User":
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
    ) -> "User":
        ...


RegisterUserAction = Callable[
    ["GraphQLContext", "RegisterInput"], Coroutine[Any, Any, "User"]
]
RegisterUserFilter = Callable[
    [RegisterUserAction, "GraphQLContext", "RegisterInput"], Coroutine[Any, Any, "User"]
]

Error = Dict[str, Any]


class ErrorsList(List[Error]):
    def add_root_error(self, error: Union[PydanticTypeError, PydanticValueError]):
        ...

    def add_error(
        self,
        location: Union[str, Sequence[str]],
        error: Union[PydanticTypeError, PydanticValueError],
    ):
        ...


GraphQLContext = Dict[str, Any]
GraphQLContextAction = Callable[
    [Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]

RegisterInput = Dict[str, Any]
RegisterInputAction = Callable[
    [
        "GraphQLContext",
        Dict[str, List[Union[AsyncRootValidator, AsyncValidator]]],
        RegisterInput,
        ErrorsList,
    ],
    Coroutine[Any, Any, Tuple[RegisterInput, ErrorsList]],
]
RegisterInputFilter = Callable[
    [RegisterInputAction, "GraphQLContext", RegisterInput],
    Coroutine[Any, Any, Tuple[RegisterInput, ErrorsList]],
]

RegisterInputModel = Type[BaseModel]
RegisterInputModelAction = Callable[
    ["GraphQLContext"], Coroutine[Any, Any, RegisterInputModel]
]
RegisterInputModelFilter = Callable[
    [RegisterInputModelAction, "GraphQLContext"],
    Coroutine[Any, Any, RegisterInputModel],
]


class SettingImage(TypedDict):
    path: str
    width: int
    height: int


Setting = Union[bool, int, str, List[str], SettingImage]
Settings = Dict[str, Setting]


class User(TypedDict):
    id: int
    name: str
    slug: str
    email: str
    email_hash: str
    password: Optional[str]
    is_moderator: bool
    is_admin: bool
    joined_at: datetime
    extra: dict
