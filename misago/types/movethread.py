from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .thread import Thread


MoveThreadInput = Dict[str, Any]
MoveThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], MoveThreadInput, ErrorsList],
    Awaitable[Tuple[MoveThreadInput, ErrorsList]],
]
MoveThreadInputFilter = Callable[
    [MoveThreadInputAction, GraphQLContext, MoveThreadInput],
    Awaitable[Tuple[MoveThreadInput, ErrorsList]],
]

MoveThreadInputModel = Type[BaseModel]
MoveThreadInputModelAction = Callable[[GraphQLContext], Awaitable[MoveThreadInputModel]]
MoveThreadInputModelFilter = Callable[
    [MoveThreadInputModelAction, GraphQLContext], Awaitable[MoveThreadInputModel],
]

MoveThreadAction = Callable[[GraphQLContext, MoveThreadInput], Awaitable[Thread]]
MoveThreadFilter = Callable[
    [MoveThreadAction, GraphQLContext, MoveThreadInput], Awaitable[Thread]
]
