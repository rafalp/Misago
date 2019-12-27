from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .thread import Thread


DeleteThreadRepliesInput = Dict[str, Any]
DeleteThreadRepliesInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[AsyncValidator]],
        DeleteThreadRepliesInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadRepliesInput, ErrorsList]],
]
DeleteThreadRepliesInputThreadFilter = Callable[
    [DeleteThreadRepliesInputThreadAction, GraphQLContext, DeleteThreadRepliesInput],
    Awaitable[Tuple[DeleteThreadRepliesInput, ErrorsList]],
]
DeleteThreadRepliesInputRepliesAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[AsyncValidator]],
        DeleteThreadRepliesInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadRepliesInput, ErrorsList]],
]
DeleteThreadRepliesInputRepliesFilter = Callable[
    [DeleteThreadRepliesInputRepliesAction, GraphQLContext, DeleteThreadRepliesInput],
    Awaitable[Tuple[DeleteThreadRepliesInput, ErrorsList]],
]

DeleteThreadRepliesInputModel = Type[BaseModel]
DeleteThreadRepliesInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadRepliesInputModel]
]
DeleteThreadRepliesInputModelFilter = Callable[
    [DeleteThreadRepliesInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadRepliesInputModel],
]

DeleteThreadRepliesAction = Callable[
    [GraphQLContext, DeleteThreadRepliesInput], Awaitable[Thread]
]
DeleteThreadRepliesFilter = Callable[
    [DeleteThreadRepliesAction, GraphQLContext, DeleteThreadRepliesInput],
    Awaitable[Thread],
]
