from typing import Any, Callable, Coroutine, Dict, List, TypedDict, Union

from starlette.requests import Request


CacheVersions = Dict[str, str]

GraphQLContext = Dict[str, Any]
GraphQLContextAction = Callable[
    [Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]


class SettingImage(TypedDict):
    path: str
    width: int
    height: int


Setting = Union[bool, int, str, List[str], SettingImage]
Settings = Dict[str, Setting]
