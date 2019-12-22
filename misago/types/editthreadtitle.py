from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .thread import Thread


EditThreadTitleInput = Dict[str, Any]
EditThreadTitleInputAction = Callable[
    [
        GraphQLContext,
        Dict[str, List[AsyncValidator]],
        EditThreadTitleInput,
        ErrorsList,
    ],
    Awaitable[Tuple[EditThreadTitleInput, ErrorsList]],
]
EditThreadTitleInputFilter = Callable[
    [EditThreadTitleInputAction, GraphQLContext, EditThreadTitleInput],
    Awaitable[Tuple[EditThreadTitleInput, ErrorsList]],
]

EditThreadTitleInputModel = Type[BaseModel]
EditThreadTitleInputModelAction = Callable[
    [GraphQLContext], Awaitable[EditThreadTitleInputModel]
]
EditThreadTitleInputModelFilter = Callable[
    [EditThreadTitleInputModelAction, GraphQLContext],
    Awaitable[EditThreadTitleInputModel],
]

EditThreadTitleAction = Callable[
    [GraphQLContext, EditThreadTitleInput], Awaitable[Thread]
]
EditThreadTitleFilter = Callable[
    [EditThreadTitleAction, GraphQLContext, EditThreadTitleInput], Awaitable[Thread]
]
