from typing import Dict, List, Tuple

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
    async def call_action(
        self,
        action: RegisterUserAction,
        context: GraphQLContext,
        cleaned_data: RegisterUserInput,
    ) -> User:
        return await self.filter(action, context, cleaned_data)


class RegisterUserInputHook(
    FilterHook[RegisterUserInputAction, RegisterUserInputFilter]
):
    async def call_action(
        self,
        action: RegisterUserInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: RegisterUserInput,
        errors_list: ErrorsList,
    ) -> Tuple[RegisterUserInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class RegisterUserInputModelHook(
    FilterHook[RegisterUserInputModelAction, RegisterUserInputModelFilter]
):
    async def call_action(
        self, action: RegisterUserInputModelAction, context: GraphQLContext
    ) -> RegisterUserInputModel:
        return await self.filter(action, context)
