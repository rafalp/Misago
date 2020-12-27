from typing import Awaitable, Dict, List, Tuple

from ..errors import ErrorsList
from ..types import (
    AsyncValidator,
    GraphQLContext,
    RegisterUserAction,
    RegisterUserFilter,
    RegisterUserInput,
    RegisterUserInputAction,
    RegisterUserInputFilter,
    RegisterUserInputModel,
    RegisterUserInputModelAction,
    RegisterUserInputModelFilter,
    User,
)

from .filter import FilterHook


class RegisterUserHook(FilterHook[RegisterUserAction, RegisterUserFilter]):
    def call_action(
        self,
        action: RegisterUserAction,
        context: GraphQLContext,
        cleaned_data: RegisterUserInput,
    ) -> Awaitable[User]:
        return self.filter(action, context, cleaned_data)


class RegisterUserInputHook(
    FilterHook[RegisterUserInputAction, RegisterUserInputFilter]
):
    def call_action(
        self,
        action: RegisterUserInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: RegisterUserInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[RegisterUserInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


class RegisterUserInputModelHook(
    FilterHook[RegisterUserInputModelAction, RegisterUserInputModelFilter]
):
    def call_action(
        self, action: RegisterUserInputModelAction, context: GraphQLContext
    ) -> Awaitable[RegisterUserInputModel]:
        return self.filter(action, context)
