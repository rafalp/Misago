from datetime import datetime

from typing import Any, Dict, List, Optional, Tuple

from starlette.requests import Request

from ..types import (
    AsyncValidator,
    AuthenticateUserAction,
    AuthenticateUserFilter,
    Category,
    CloseThreadAction,
    CloseThreadFilter,
    CloseThreadInput,
    CloseThreadInputAction,
    CloseThreadInputFilter,
    CloseThreadInputModel,
    CloseThreadInputModelAction,
    CloseThreadInputModelFilter,
    CreatePostAction,
    CreatePostFilter,
    CreateThreadAction,
    CreateThreadFilter,
    CreateUserAction,
    CreateUserFilter,
    CreateUserTokenAction,
    CreateUserTokenFilter,
    CreateUserTokenPayloadAction,
    CreateUserTokenPayloadFilter,
    EditPostInput,
    EditPostInputAction,
    EditPostInputFilter,
    EditPostInputModel,
    EditPostInputModelAction,
    EditPostInputModelFilter,
    EditPostAction,
    EditPostFilter,
    EditThreadTitleInput,
    EditThreadTitleInputAction,
    EditThreadTitleInputFilter,
    EditThreadTitleInputModel,
    EditThreadTitleInputModelAction,
    EditThreadTitleInputModelFilter,
    EditThreadTitleAction,
    EditThreadTitleFilter,
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
    PostReplyAction,
    PostReplyFilter,
    PostReplyInput,
    PostReplyInputAction,
    PostReplyInputFilter,
    PostReplyInputModel,
    PostReplyInputModelAction,
    PostReplyInputModelFilter,
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


class CloseThreadHook(FilterHook[CloseThreadAction, CloseThreadFilter]):
    async def call_action(
        self,
        action: CloseThreadAction,
        context: GraphQLContext,
        cleaned_data: CloseThreadInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class CloseThreadInputHook(FilterHook[CloseThreadInputAction, CloseThreadInputFilter]):
    async def call_action(
        self,
        action: CloseThreadInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: CloseThreadInput,
        errors_list: ErrorsList,
    ) -> Tuple[CloseThreadInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class CloseThreadInputModelHook(
    FilterHook[CloseThreadInputModelAction, CloseThreadInputModelFilter]
):
    async def call_action(
        self, action: CloseThreadInputModelAction, context: GraphQLContext
    ) -> CloseThreadInputModel:
        return await self.filter(action, context)


class CreatePostHook(FilterHook[CreatePostAction, CreatePostFilter]):
    async def call_action(
        self,
        action: CreatePostAction,
        thread: Thread,
        body: dict,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[dict] = None,
    ) -> Post:
        return await self.filter(
            action,
            thread,
            body,
            poster=poster,
            poster_name=poster_name,
            edits=edits,
            posted_at=posted_at,
            extra=extra,
        )


class CreateThreadHook(FilterHook[CreateThreadAction, CreateThreadFilter]):
    async def call_action(
        self,
        action: CreateThreadAction,
        category: Category,
        title: str,
        *,
        first_post: Optional[Post] = None,
        starter: Optional[User] = None,
        starter_name: Optional[str] = None,
        replies: int = 0,
        is_closed: bool = False,
        started_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Thread:
        return await self.filter(
            action,
            category,
            title,
            first_post=first_post,
            starter=starter,
            starter_name=starter_name,
            replies=replies,
            is_closed=is_closed,
            started_at=started_at,
            extra=extra,
        )


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
        extra: Optional[Dict[str, Any]] = None,
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


class EditPostHook(FilterHook[EditPostAction, EditPostFilter]):
    async def call_action(
        self,
        action: EditPostAction,
        context: GraphQLContext,
        cleaned_data: EditPostInput,
    ) -> Tuple[Thread, Post]:
        return await self.filter(action, context, cleaned_data)


class EditPostInputHook(FilterHook[EditPostInputAction, EditPostInputFilter]):
    async def call_action(
        self,
        action: EditPostInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: EditPostInput,
        errors_list: ErrorsList,
    ) -> Tuple[EditPostInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class EditPostInputModelHook(
    FilterHook[EditPostInputModelAction, EditPostInputModelFilter]
):
    async def call_action(
        self, action: EditPostInputModelAction, context: GraphQLContext
    ) -> EditPostInputModel:
        return await self.filter(action, context)


class EditThreadTitleHook(FilterHook[EditThreadTitleAction, EditThreadTitleFilter]):
    async def call_action(
        self,
        action: EditThreadTitleAction,
        context: GraphQLContext,
        cleaned_data: EditThreadTitleInput,
    ) -> Thread:
        return await self.filter(action, context, cleaned_data)


class EditThreadTitleInputHook(
    FilterHook[EditThreadTitleInputAction, EditThreadTitleInputFilter]
):
    async def call_action(
        self,
        action: EditThreadTitleInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: EditThreadTitleInput,
        errors_list: ErrorsList,
    ) -> Tuple[EditThreadTitleInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class EditThreadTitleInputModelHook(
    FilterHook[EditThreadTitleInputModelAction, EditThreadTitleInputModelFilter]
):
    async def call_action(
        self, action: EditThreadTitleInputModelAction, context: GraphQLContext
    ) -> EditThreadTitleInputModel:
        return await self.filter(action, context)


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


class PostReplyHook(FilterHook[PostReplyAction, PostReplyFilter]):
    async def call_action(
        self,
        action: PostReplyAction,
        context: GraphQLContext,
        cleaned_data: PostReplyInput,
    ) -> Tuple[Thread, Post]:
        return await self.filter(action, context, cleaned_data)


class PostReplyInputHook(FilterHook[PostReplyInputAction, PostReplyInputFilter]):
    async def call_action(
        self,
        action: PostReplyInputAction,
        context: GraphQLContext,
        validators: Dict[str, List[AsyncValidator]],
        data: PostReplyInput,
        errors_list: ErrorsList,
    ) -> Tuple[PostReplyInput, ErrorsList]:
        return await self.filter(action, context, validators, data, errors_list)


class PostReplyInputModelHook(
    FilterHook[PostReplyInputModelAction, PostReplyInputModelFilter]
):
    async def call_action(
        self, action: PostReplyInputModelAction, context: GraphQLContext
    ) -> PostReplyInputModel:
        return await self.filter(action, context)


class PostThreadHook(FilterHook[PostThreadAction, PostThreadFilter]):
    async def call_action(
        self,
        action: PostThreadAction,
        context: GraphQLContext,
        cleaned_data: PostThreadInput,
    ) -> Tuple[Thread, Post]:
        return await self.filter(action, context, cleaned_data)


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
