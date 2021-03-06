from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .validator import Validator

DeleteThreadInput = Dict[str, Any]
DeleteThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], DeleteThreadInput, ErrorsList],
    Awaitable[Tuple[DeleteThreadInput, ErrorsList]],
]
DeleteThreadInputFilter = Callable[
    [DeleteThreadInputAction, GraphQLContext, DeleteThreadInput],
    Awaitable[Tuple[DeleteThreadInput, ErrorsList]],
]

DeleteThreadInputModel = Type[BaseModel]
DeleteThreadInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadInputModel]
]
DeleteThreadInputModelFilter = Callable[
    [DeleteThreadInputModelAction, GraphQLContext], Awaitable[DeleteThreadInputModel],
]

DeleteThreadAction = Callable[[GraphQLContext, DeleteThreadInput], Awaitable[None]]
DeleteThreadFilter = Callable[
    [DeleteThreadAction, GraphQLContext, DeleteThreadInput], Awaitable[None]
]
