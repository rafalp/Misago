from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext


DeleteThreadsInput = Dict[str, Any]
DeleteThreadsInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], DeleteThreadsInput, ErrorsList],
    Awaitable[Tuple[DeleteThreadsInput, ErrorsList]],
]
DeleteThreadsInputFilter = Callable[
    [DeleteThreadsInputAction, GraphQLContext, DeleteThreadsInput],
    Awaitable[Tuple[DeleteThreadsInput, ErrorsList]],
]

DeleteThreadsInputModel = Type[BaseModel]
DeleteThreadsInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadsInputModel]
]
DeleteThreadsInputModelFilter = Callable[
    [DeleteThreadsInputModelAction, GraphQLContext], Awaitable[DeleteThreadsInputModel],
]

DeleteThreadsAction = Callable[[GraphQLContext, DeleteThreadsInput], Awaitable[None]]
DeleteThreadsFilter = Callable[
    [DeleteThreadsAction, GraphQLContext, DeleteThreadsInput], Awaitable[None]
]
