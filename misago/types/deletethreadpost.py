from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .thread import Thread
from .validator import Validator

DeleteThreadPostInput = Dict[str, Any]
DeleteThreadPostInputThreadAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], DeleteThreadPostInput, ErrorsList,],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]
DeleteThreadPostInputThreadFilter = Callable[
    [DeleteThreadPostInputThreadAction, GraphQLContext, DeleteThreadPostInput],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]
DeleteThreadPostInputPostAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], DeleteThreadPostInput, ErrorsList,],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]
DeleteThreadPostInputPostFilter = Callable[
    [DeleteThreadPostInputPostAction, GraphQLContext, DeleteThreadPostInput],
    Awaitable[Tuple[DeleteThreadPostInput, ErrorsList]],
]

DeleteThreadPostInputModel = Type[BaseModel]
DeleteThreadPostInputModelAction = Callable[
    [GraphQLContext], Awaitable[DeleteThreadPostInputModel]
]
DeleteThreadPostInputModelFilter = Callable[
    [DeleteThreadPostInputModelAction, GraphQLContext],
    Awaitable[DeleteThreadPostInputModel],
]

DeleteThreadPostAction = Callable[
    [GraphQLContext, DeleteThreadPostInput], Awaitable[Thread]
]
DeleteThreadPostFilter = Callable[
    [DeleteThreadPostAction, GraphQLContext, DeleteThreadPostInput], Awaitable[Thread]
]
