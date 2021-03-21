from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .thread import Thread
from .validator import Validator

DeleteThreadPostsInput = Dict[str, Any]
DeleteThreadPostsInputThreadAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        DeleteThreadPostsInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]
DeleteThreadPostsInputThreadFilter = Callable[
    [DeleteThreadPostsInputThreadAction, GraphQLContext, DeleteThreadPostsInput],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]
DeleteThreadPostsInputPostsAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        DeleteThreadPostsInput,
        ErrorsList,
    ],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]
DeleteThreadPostsInputPostsFilter = Callable[
    [DeleteThreadPostsInputPostsAction, GraphQLContext, DeleteThreadPostsInput],
    Awaitable[Tuple[DeleteThreadPostsInput, ErrorsList]],
]

DeleteThreadPostsInputModel = Type[BaseModel]
DeleteThreadPostsInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadPostsInputModel]
]
DeleteThreadPostsInputModelFilter = Callable[
    [DeleteThreadPostsInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadPostsInputModel],
]

DeleteThreadPostsAction = Callable[
    [GraphQLContext, DeleteThreadPostsInput], Awaitable[Thread]
]
DeleteThreadPostsFilter = Callable[
    [DeleteThreadPostsAction, GraphQLContext, DeleteThreadPostsInput],
    Awaitable[Thread],
]
