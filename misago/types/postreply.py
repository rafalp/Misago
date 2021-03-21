from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .graphqlcontext import GraphQLContext
from .parsemarkup import ParsedMarkupMetadata
from .post import Post
from .thread import Thread
from .validator import Validator

PostReplyInput = Dict[str, Any]
PostReplyInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[Validator]],
        PostReplyInput,
        ErrorsList,
    ],
    Awaitable[Tuple[PostReplyInput, ErrorsList]],
]
PostReplyInputFilter = Callable[
    [PostReplyInputAction, GraphQLContext, PostReplyInput],
    Awaitable[Tuple[PostReplyInput, ErrorsList]],
]

PostReplyInputModel = Type[BaseModel]
PostReplyInputModelAction = Callable[[GraphQLContext], Awaitable[PostReplyInputModel]]
PostReplyInputModelFilter = Callable[
    [PostReplyInputModelAction, GraphQLContext],
    Awaitable[PostReplyInputModel],
]

PostReplyAction = Callable[
    [GraphQLContext, PostReplyInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
PostReplyFilter = Callable[
    [PostReplyAction, GraphQLContext, PostReplyInput],
    Awaitable[Tuple[Thread, Post, ParsedMarkupMetadata]],
]
