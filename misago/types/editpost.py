from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata
from .post import Post
from .thread import Thread
from .validator import Validator

EditPostInput = Dict[str, Any]
EditPostInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], EditPostInput, ErrorsList,],
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
    [GraphQLContext, EditPostInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
EditPostFilter = Callable[
    [EditPostAction, GraphQLContext, EditPostInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
