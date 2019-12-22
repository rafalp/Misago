from typing import Any, Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor

from .action import ActionHook
from .filter import FilterHook
from .filters import (
    AuthenticateUserHook,
    CloseThreadHook,
    CloseThreadInputHook,
    CloseThreadInputModelHook,
    CreatePostHook,
    CreateThreadHook,
    CreateUserHook,
    CreateUserTokenHook,
    CreateUserTokenPayloadHook,
    EditPostHook,
    EditPostInputHook,
    EditPostInputModelHook,
    EditThreadTitleHook,
    EditThreadTitleInputHook,
    EditThreadTitleInputModelHook,
    GetAuthUserHook,
    GetUserFromContextHook,
    GetUserFromTokenHook,
    GetUserFromTokenPayloadHook,
    GraphQLContextHook,
    PostReplyHook,
    PostReplyInputHook,
    PostReplyInputModelHook,
    PostThreadHook,
    PostThreadInputHook,
    PostThreadInputModelHook,
    RegisterUserHook,
    RegisterUserInputHook,
    RegisterUserInputModelHook,
    TemplateContextHook,
)


authenticate_user_hook = AuthenticateUserHook()
close_thread_hook = CloseThreadHook()
close_thread_input_hook = CloseThreadInputHook()
close_thread_input_model_hook = CloseThreadInputModelHook()
create_post_hook = CreatePostHook()
create_thread_hook = CreateThreadHook()
create_user_hook = CreateUserHook()
create_user_token_hook = CreateUserTokenHook()
create_user_token_payload_hook = CreateUserTokenPayloadHook()
edit_post_hook = EditPostHook()
edit_post_input_hook = EditPostInputHook()
edit_post_input_model_hook = EditPostInputModelHook()
edit_thread_title_hook = EditThreadTitleHook()
edit_thread_title_input_hook = EditThreadTitleInputHook()
edit_thread_title_input_model_hook = EditThreadTitleInputModelHook()
get_auth_user_hook = GetAuthUserHook()
get_user_from_context_hook = GetUserFromContextHook()
get_user_from_token_hook = GetUserFromTokenHook()
get_user_from_token_payload_hook = GetUserFromTokenPayloadHook()
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
jinja2_extensions: List[Any] = []
jinja2_filters: Dict[str, Any] = {}
post_reply_hook = PostReplyHook()
post_reply_input_hook = PostReplyInputHook()
post_reply_input_model_hook = PostReplyInputModelHook()
post_thread_hook = PostThreadHook()
post_thread_input_hook = PostThreadInputHook()
post_thread_input_model_hook = PostThreadInputModelHook()
register_user_hook = RegisterUserHook()
register_user_input_hook = RegisterUserInputHook()
register_user_input_model_hook = RegisterUserInputModelHook()
template_context_hook = TemplateContextHook()
