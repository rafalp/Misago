from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .thread import Thread
from .validator import Validator

CloseThreadsInput = Dict[str, Any]
CloseThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], CloseThreadsInput, ErrorsList],
    Awaitable[Tuple[CloseThreadsInput, ErrorsList]],
]
CloseThreadsInputFilter = Callable[
    [CloseThreadsInputAction, GraphQLContext, CloseThreadsInput],
    Awaitable[Tuple[CloseThreadsInput, ErrorsList]],
]

CloseThreadsInputModel = Type[BaseModel]
CloseThreadsInputModelAction = Callable[
    [GraphQLContext], Awaitable[CloseThreadsInputModel]
]
CloseThreadsInputModelFilter = Callable[
    [CloseThreadsInputModelAction, GraphQLContext],
    Awaitable[CloseThreadsInputModel],
]

CloseThreadsAction = Callable[
    [GraphQLContext, CloseThreadsInput], Awaitable[List[Thread]]
]
CloseThreadsFilter = Callable[
    [CloseThreadsAction, GraphQLContext, CloseThreadsInput], Awaitable[List[Thread]]
]
