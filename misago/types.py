from typing import Any, Callable, Coroutine, Dict, List, Optional, TypedDict, Union

from starlette.requests import Request


CacheVersions = Dict[str, str]

GraphQLContext = Dict[str, Any]
GraphQLContextAction = Callable[
    [Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]
GraphQLContextFilter = Callable[
    [GraphQLContextAction, Request, GraphQLContext], Coroutine[Any, Any, GraphQLContext]
]


class Setting(TypedDict):
    value: "SettingValue"
    width: Optional[int]
    height: Optional[int]


Settings = Dict[str, "Setting"]
SettingValue = Union[bool, int, str, List[str]]
