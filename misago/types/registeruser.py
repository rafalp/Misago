from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from ..errors import ErrorsList
from .asyncvalidator import AsyncValidator
from .graphqlcontext import GraphQLContext
from .user import User


RegisterUserInput = Dict[str, Any]
RegisterUserInputAction = Callable[
    [GraphQLContext, Dict[str, List[AsyncValidator]], RegisterUserInput, ErrorsList],
    Awaitable[Tuple[RegisterUserInput, ErrorsList]],
]
RegisterUserInputFilter = Callable[
    [RegisterUserInputAction, GraphQLContext, RegisterUserInput],
    Awaitable[Tuple[RegisterUserInput, ErrorsList]],
]

RegisterUserInputModel = Type[BaseModel]
RegisterUserInputModelAction = Callable[
    [GraphQLContext], Awaitable[RegisterUserInputModel]
]
RegisterUserInputModelFilter = Callable[
    [RegisterUserInputModelAction, GraphQLContext], Awaitable[RegisterUserInputModel],
]

RegisterUserAction = Callable[[GraphQLContext, RegisterUserInput], Awaitable[User]]
RegisterUserFilter = Callable[
    [RegisterUserAction, GraphQLContext, RegisterUserInput], Awaitable[User]
]
