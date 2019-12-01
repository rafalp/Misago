from typing import Dict, List, Tuple, Union

from starlette.requests import Request

from ..types import (
    AsyncRootValidator,
    AsyncValidator,
    ErrorsList,
    GraphQLContext,
    GraphQLContextAction,
    GraphQLContextFilter,
    RegisterInput,
    RegisterInputAction,
    RegisterInputFilter,
    RegisterInputModel,
    RegisterInputModelAction,
    RegisterInputModelFilter,
)
from .filter import FilterHook


class GraphQLContextHook(FilterHook[GraphQLContextAction, GraphQLContextFilter]):
    async def call_action(
        self, action: GraphQLContextAction, request: Request, context: GraphQLContext
    ) -> GraphQLContext:
        return await self.filter(action, request, context)


class RegisterInputHook(FilterHook[RegisterInputAction, RegisterInputFilter]):
    async def call_action(
        self,
        action: RegisterInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[Union[AsyncRootValidator, AsyncValidator]]],
        data: RegisterInput,
        errors_list: ErrorsList,
    ) -> Tuple[RegisterInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class RegisterInputModelHook(
    FilterHook[RegisterInputModelAction, RegisterInputModelFilter]
):
    async def call_action(
        self, action: RegisterInputModelAction, context: GraphQLContext
    ) -> RegisterInputModel:
        return await self.filter(action, context)
