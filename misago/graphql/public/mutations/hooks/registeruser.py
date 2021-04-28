from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....types import Validator
from .....users.models import User
from .... import GraphQLContext

RegisterUserInputModel = Type[BaseModel]
RegisterUserInputModelAction = Callable[
    [GraphQLContext], Awaitable[RegisterUserInputModel]
]
RegisterUserInputModelFilter = Callable[
    [RegisterUserInputModelAction, GraphQLContext],
    Awaitable[RegisterUserInputModel],
]


class RegisterUserInputModelHook(
    FilterHook[RegisterUserInputModelAction, RegisterUserInputModelFilter]
):
    def call_action(
        self, action: RegisterUserInputModelAction, context: GraphQLContext
    ) -> Awaitable[RegisterUserInputModel]:
        return self.filter(action, context)


RegisterUserInput = Dict[str, Any]
RegisterUserInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], RegisterUserInput, ErrorsList],
    Awaitable[Tuple[RegisterUserInput, ErrorsList]],
]
RegisterUserInputFilter = Callable[
    [RegisterUserInputAction, GraphQLContext, RegisterUserInput],
    Awaitable[Tuple[RegisterUserInput, ErrorsList]],
]


class RegisterUserInputHook(
    FilterHook[RegisterUserInputAction, RegisterUserInputFilter]
):
    def call_action(
        self,
        action: RegisterUserInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: RegisterUserInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[RegisterUserInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


RegisterUserAction = Callable[[GraphQLContext, RegisterUserInput], Awaitable[User]]
RegisterUserFilter = Callable[
    [RegisterUserAction, GraphQLContext, RegisterUserInput], Awaitable[User]
]


class RegisterUserHook(FilterHook[RegisterUserAction, RegisterUserFilter]):
    def call_action(
        self,
        action: RegisterUserAction,
        context: GraphQLContext,
        cleaned_data: RegisterUserInput,
    ) -> Awaitable[User]:
        return self.filter(action, context, cleaned_data)


register_user_hook = RegisterUserHook()
register_user_input_hook = RegisterUserInputHook()
register_user_input_model_hook = RegisterUserInputModelHook()
