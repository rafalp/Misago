from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .thread import Thread


DeleteThreadReplyInput = Dict[str, Any]
DeleteThreadReplyInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[AsyncValidator]],
        DeleteThreadReplyInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadReplyInput, ErrorsList]],
]
DeleteThreadReplyInputThreadFilter = Callable[
    [DeleteThreadReplyInputThreadAction, GraphQLContext, DeleteThreadReplyInput],
    Awaitable[Tuple[DeleteThreadReplyInput, ErrorsList]],
]
DeleteThreadReplyInputReplyAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[AsyncValidator]],
        DeleteThreadReplyInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadReplyInput, ErrorsList]],
]
DeleteThreadReplyInputReplyFilter = Callable[
    [DeleteThreadReplyInputReplyAction, GraphQLContext, DeleteThreadReplyInput],
    Awaitable[Tuple[DeleteThreadReplyInput, ErrorsList]],
]

DeleteThreadReplyInputModel = Type[BaseModel]
DeleteThreadReplyInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadReplyInputModel]
]
DeleteThreadReplyInputModelFilter = Callable[
    [DeleteThreadReplyInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadReplyInputModel],
]

DeleteThreadReplyAction = Callable[
    [GraphQLContext, DeleteThreadReplyInput], Awaitable[Thread]
]
DeleteThreadReplyFilter = Callable[
    [DeleteThreadReplyAction, GraphQLContext, DeleteThreadReplyInput], Awaitable[Thread]
]
