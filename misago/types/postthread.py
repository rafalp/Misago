from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .post import Post
from .thread import Thread


PostThreadInput = Dict[str, Any]
PostThreadInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], PostThreadInput, ErrorsList,],
    Awaitable[Tuple[PostThreadInput, ErrorsList]],
]
PostThreadInputFilter = Callable[
    [PostThreadInputAction, GraphQLContext, PostThreadInput],
    Awaitable[Tuple[PostThreadInput, ErrorsList]],
]

PostThreadInputModel = Type[BaseModel]
PostThreadInputModelAction = Callable[[GraphQLContext], Awaitable[PostThreadInputModel]]
PostThreadInputModelFilter = Callable[
    [PostThreadInputModelAction, GraphQLContext], Awaitable[PostThreadInputModel],
]

PostThreadAction = Callable[
    [GraphQLContext, PostThreadInput], Awaitable[Tuple[Thread, Post]]
]
PostThreadFilter = Callable[
    [PostThreadAction, GraphQLContext, PostThreadInput], Awaitable[Tuple[Thread, Post]],
]
