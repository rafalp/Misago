from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .thread import Thread


CloseThreadsInput = Dict[str, Any]
CloseThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], CloseThreadsInput, ErrorsList],
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
    [CloseThreadsInputModelAction, GraphQLContext], Awaitable[CloseThreadsInputModel],
]

CloseThreadsAction = Callable[
    [GraphQLContext, CloseThreadsInput], Awaitable[List[Thread]]
]
CloseThreadsFilter = Callable[
    [CloseThreadsAction, GraphQLContext, CloseThreadsInput], Awaitable[List[Thread]]
]
