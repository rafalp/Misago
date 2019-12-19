from datetime import datetime

from typing import Any, Dict, List, Optional, Tuple

from starlette.requests import Request

from ..types import (
    AsyncValidator,
    AuthenticateUserAction,
    AuthenticateUserFilter,
    CreateUserAction,
    CreateUserFilter,
    CreateUserTokenAction,
    CreateUserTokenFilter,
    CreateUserTokenPayloadAction,
    CreateUserTokenPayloadFilter,
    ErrorsList,
    GetAuthUserAction,
    GetAuthUserFilter,
    GetUserFromContextAction,
    GetUserFromContextFilter,
    GetUserFromTokenAction,
    GetUserFromTokenFilter,
    GetUserFromTokenPayloadAction,
    GetUserFromTokenPayloadFilter,
    GraphQLContext,
    GraphQLContextAction,
    GraphQLContextFilter,
    Post,
    PostThreadAction,
    PostThreadFilter,
    PostThreadInput,
    PostThreadInputAction,
    PostThreadInputFilter,
    PostThreadInputModel,
    PostThreadInputModelAction,
    PostThreadInputModelFilter,
    RegisterInput,
    RegisterInputAction,
    RegisterInputFilter,
    RegisterInputModel,
    RegisterInputModelAction,
    RegisterInputModelFilter,
    RegisterUserAction,
    RegisterUserFilter,
    TemplateContext,
    TemplateContextAction,
    TemplateContextFilter,
    Thread,
    User,
)
from .filter import FilterHook


class AuthenticateUserHook(FilterHook[AuthenticateUserAction, AuthenticateUserFilter]):
    async def call_action(
        self,
        action: AuthenticateUserAction,
        context: GraphQLContext,
        username: str,
        password: str,
    ) -> Optional[User]:
        return await self.filter(action, context, username, password)


class CreateUserHook(FilterHook[CreateUserAction, CreateUserFilter]):
    async def call_action(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_deactivated: bool = False,
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
            is_deactivated=is_deactivated,
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


class GetAuthUserHook(FilterHook[GetAuthUserAction, GetAuthUserFilter]):
    async def call_action(
        self, action: GetAuthUserAction, context: GraphQLContext, user_id: int
    ) -> Optional[User]:
        return await self.filter(action, context, user_id)


class GetUserFromContextHook(
    FilterHook[GetUserFromContextAction, GetUserFromContextFilter]
):
    async def call_action(
        self, action: GetUserFromContextAction, context: GraphQLContext
    ) -> Optional[User]:
        return await self.filter(action, context)


class GetUserFromTokenHook(FilterHook[GetUserFromTokenAction, GetUserFromTokenFilter]):
    async def call_action(
        self, action: GetUserFromTokenAction, context: GraphQLContext, token: str
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


class PostThreadInputHook(FilterHook[PostThreadInputAction, PostThreadInputFilter]):
    async def call_action(
        self,
        action: PostThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: PostThreadInput,
        errors_list: ErrorsList,
    ) -> Tuple[PostThreadInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class PostThreadInputModelHook(
    FilterHook[PostThreadInputModelAction, PostThreadInputModelFilter]
):
    async def call_action(
        self, action: PostThreadInputModelAction, context: GraphQLContext
    ) -> PostThreadInputModel:
        return await self.filter(action, context)


class PostThreadHook(FilterHook[PostThreadAction, PostThreadFilter]):
    async def call_action(
        self,
        action: PostThreadAction,
        context: GraphQLContext,
        cleaned_data: PostThreadInput,
    ) -> Tuple[Thread, Post]:
        return await self.filter(action, context, cleaned_data)


class RegisterInputHook(FilterHook[RegisterInputAction, RegisterInputFilter]):
    async def call_action(
        self,
        action: RegisterInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
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


class TemplateContextHook(FilterHook[TemplateContextAction, TemplateContextFilter]):
    async def call_action(
        self, action: TemplateContextAction, request: Request
    ) -> TemplateContext:
        return await self.filter(action, request)
