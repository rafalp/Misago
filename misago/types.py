from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
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
