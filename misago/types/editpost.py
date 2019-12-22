from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .post import Post
from .thread import Thread


EditPostInput = Dict[str, Any]
EditPostInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], EditPostInput, ErrorsList,],
    Awaitable[Tuple[EditPostInput, ErrorsList]],
]
EditPostInputFilter = Callable[
    [EditPostInputAction, GraphQLContext, EditPostInput],
    Awaitable[Tuple[EditPostInput, ErrorsList]],
]

EditPostInputModel = Type[BaseModel]
EditPostInputModelAction = Callable[[GraphQLContext], Awaitable[EditPostInputModel]]
EditPostInputModelFilter = Callable[
    [EditPostInputModelAction, GraphQLContext], Awaitable[EditPostInputModel],
]

EditPostAction = Callable[
    [GraphQLContext, EditPostInput], Awaitable[Tuple[Thread, Post]]
]
EditPostFilter = Callable[
    [EditPostAction, GraphQLContext, EditPostInput], Awaitable[Tuple[Thread, Post]],
]
