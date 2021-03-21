from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .thread import Thread
from .validator import Validator

MoveThreadsInput = Dict[str, Any]
MoveThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], MoveThreadsInput, ErrorsList],
    Awaitable[Tuple[MoveThreadsInput, ErrorsList]],
]
MoveThreadsInputFilter = Callable[
    [MoveThreadsInputAction, GraphQLContext, MoveThreadsInput],
    Awaitable[Tuple[MoveThreadsInput, ErrorsList]],
]

MoveThreadsInputModel = Type[BaseModel]
MoveThreadsInputModelAction = Callable[
    [GraphQLContext], Awaitable[MoveThreadsInputModel]
]
MoveThreadsInputModelFilter = Callable[
    [MoveThreadsInputModelAction, GraphQLContext],
    Awaitable[MoveThreadsInputModel],
]

MoveThreadsAction = Callable[
    [GraphQLContext, MoveThreadsInput], Awaitable[List[Thread]]
]
MoveThreadsFilter = Callable[
    [MoveThreadsAction, GraphQLContext, MoveThreadsInput], Awaitable[List[Thread]]
]
