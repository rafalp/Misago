from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .thread import Thread


CloseThreadInput = Dict[str, Any]
CloseThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], CloseThreadInput, ErrorsList],
    Awaitable[Tuple[CloseThreadInput, ErrorsList]],
]
CloseThreadInputFilter = Callable[
    [CloseThreadInputAction, GraphQLContext, CloseThreadInput],
    Awaitable[Tuple[CloseThreadInput, ErrorsList]],
]

CloseThreadInputModel = Type[BaseModel]
CloseThreadInputModelAction = Callable[
    [GraphQLContext], Awaitable[CloseThreadInputModel]
]
CloseThreadInputModelFilter = Callable[
    [CloseThreadInputModelAction, GraphQLContext], Awaitable[CloseThreadInputModel],
]

CloseThreadAction = Callable[[GraphQLContext, CloseThreadInput], Awaitable[Thread]]
CloseThreadFilter = Callable[
    [CloseThreadAction, GraphQLContext, CloseThreadInput], Awaitable[Thread]
]
