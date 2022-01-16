from typing import Any, Awaitable, Callable, Dict, List, Tuple, Type

from pydantic import BaseModel

from .....errors import ErrorsList
from .....hooks import FilterHook
from .....users.models import User
from .....validation import Validator
from .... import GraphQLContext

UserCreateInputModel = Type[BaseModel]
UserCreateInputModelAction = Callable[[GraphQLContext], Awaitable[UserCreateInputModel]]
UserCreateInputModelFilter = Callable[
    [UserCreateInputModelAction, GraphQLContext],
    Awaitable[UserCreateInputModel],
]


class UserCreateInputModelHook(
    FilterHook[UserCreateInputModelAction, UserCreateInputModelFilter]
):
    def call_action(
        self, action: UserCreateInputModelAction, context: GraphQLContext
    ) -> Awaitable[UserCreateInputModel]:
        return self.filter(action, context)


UserCreateInput = Dict[str, Any]
UserCreateInputAction = Callable[
    [GraphQLContext, Dict[str, List[Validator]], UserCreateInput, ErrorsList],
    Awaitable[Tuple[UserCreateInput, ErrorsList]],
]
UserCreateInputFilter = Callable[
    [UserCreateInputAction, GraphQLContext, UserCreateInput],
    Awaitable[Tuple[UserCreateInput, ErrorsList]],
]


class UserCreateInputHook(FilterHook[UserCreateInputAction, UserCreateInputFilter]):
    def call_action(
        self,
        action: UserCreateInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Validator]],
        data: UserCreateInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[UserCreateInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


UserCreateAction = Callable[[GraphQLContext, UserCreateInput], Awaitable[User]]
UserCreateFilter = Callable[
    [UserCreateAction, GraphQLContext, UserCreateInput], Awaitable[User]
]


class UserCreateHook(FilterHook[UserCreateAction, UserCreateFilter]):
    def call_action(
        self,
        action: UserCreateAction,
        context: GraphQLContext,
        cleaned_data: UserCreateInput,
    ) -> Awaitable[User]:
        return self.filter(action, context, cleaned_data)


user_create_hook = UserCreateHook()
user_create_input_hook = UserCreateInputHook()
user_create_input_model_hook = UserCreateInputModelHook()
