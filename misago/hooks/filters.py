from datetime import datetime

from typing import Any, Dict, List, Optional, Tuple, Union

from starlette.requests import Request

from ..types import (
    AsyncRootValidator,
    AsyncValidator,
    CreateUserAction,
    CreateUserFilter,
    CreateUserTokenAction,
    CreateUserTokenFilter,
    CreateUserTokenPayloadAction,
    CreateUserTokenPayloadFilter,
    ErrorsList,
    GetUserFromTokenAction,
    GetUserFromTokenFilter,
    GetUserFromTokenPayloadAction,
    GetUserFromTokenPayloadFilter,
    GraphQLContext,
    GraphQLContextAction,
    GraphQLContextFilter,
    RegisterInput,
    RegisterInputAction,
    RegisterInputFilter,
    RegisterInputModel,
    RegisterInputModelAction,
    RegisterInputModelFilter,
    RegisterUserAction,
    RegisterUserFilter,
    User,
)
from .filter import FilterHook


class CreateUserHook(FilterHook[CreateUserAction, CreateUserFilter]):
    async def call_action(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_disabled: bool = False,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None
    ) -> User:
        return await self.filter(
            action,
            name,
            email,
            password=password,
            is_disabled=is_disabled,
            is_moderator=is_moderator,
            is_admin=is_admin,
            joined_at=joined_at,
            extra=extra,
        )


class CreateUserTokenHook(FilterHook[CreateUserTokenAction, CreateUserTokenFilter]):
    async def call_action(
        self, action: CreateUserTokenAction, context: GraphQLContext, user: User,
    ) -> str:
        return await self.filter(action, context, user)


class CreateUserTokenPayloadHook(
    FilterHook[CreateUserTokenPayloadAction, CreateUserTokenPayloadFilter]
):
    async def call_action(
        self, action: CreateUserTokenPayloadAction, context: GraphQLContext, user: User,
    ) -> Dict[str, Any]:
        return await self.filter(action, context, user)


class GetUserFromTokenHook(FilterHook[GetUserFromTokenAction, GetUserFromTokenFilter]):
    async def call_action(
        self, action: GetUserFromTokenAction, context: GraphQLContext, token: bytes
    ) -> Optional[User]:
        return await self.filter(action, context, token)


class GetUserFromTokenPayloadHook(
    FilterHook[GetUserFromTokenPayloadAction, GetUserFromTokenPayloadFilter]
):
    async def call_action(
        self,
        action: GetUserFromTokenPayloadAction,
        context: GraphQLContext,
        token_payload: Dict[str, Any],
    ) -> Optional[User]:
        return await self.filter(action, context, token_payload)


class GraphQLContextHook(FilterHook[GraphQLContextAction, GraphQLContextFilter]):
    async def call_action(
        self, action: GraphQLContextAction, request: Request
    ) -> GraphQLContext:
        return await self.filter(action, request)


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


class RegisterUserHook(FilterHook[RegisterUserAction, RegisterUserFilter]):
    async def call_action(
        self,
        action: RegisterUserAction,
        context: GraphQLContext,
        cleaned_data: RegisterInput,
    ) -> User:
        return await self.filter(action, context, cleaned_data)
