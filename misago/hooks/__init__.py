from typing import Any, Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor

from .action import ActionHook
from .authenticateuser import AuthenticateUserHook
from .closethread import (
    CloseThreadHook,
    CloseThreadInputHook,
    CloseThreadInputModelHook,
)
from .closethreads import (
    CloseThreadsHook,
    CloseThreadsInputHook,
    CloseThreadsInputModelHook,
)
from .convertblockasttorichtext import ConvertBlockAstToRichTextHook
from .convertinlineasttotext import ConvertInlineAstToTextHook
from .createmarkdown import CreateMarkdownHook
from .createpost import CreatePostHook
from .createthread import CreateThreadHook
from .createuser import CreateUserHook
from .createusertoken import CreateUserTokenHook, CreateUserTokenPayloadHook
from .deletethread import (
    DeleteThreadHook,
    DeleteThreadInputHook,
    DeleteThreadInputModelHook,
)
from .deletethreadpost import (
    DeleteThreadPostHook,
    DeleteThreadPostInputModelHook,
    DeleteThreadPostInputPostHook,
    DeleteThreadPostInputThreadHook,
)
from .deletethreadposts import (
    DeleteThreadPostsHook,
    DeleteThreadPostsInputModelHook,
    DeleteThreadPostsInputPostsHook,
    DeleteThreadPostsInputThreadHook,
)
from .deletethreads import (
    DeleteThreadsHook,
    DeleteThreadsInputHook,
    DeleteThreadsInputModelHook,
)
from .editpost import EditPostHook, EditPostInputHook, EditPostInputModelHook
from .editthreadtitle import (
    EditThreadTitleHook,
    EditThreadTitleInputHook,
    EditThreadTitleInputModelHook,
)
from .filter import FilterHook
from .graphqlcontext import GraphQLContextHook
from .movethread import MoveThreadHook, MoveThreadInputHook, MoveThreadInputModelHook
from .movethreads import (
    MoveThreadsHook,
    MoveThreadsInputHook,
    MoveThreadsInputModelHook,
)
from .parsemarkup import ParseMarkupHook
from .postreply import PostReplyHook, PostReplyInputHook, PostReplyInputModelHook
from .postthread import PostThreadHook, PostThreadInputHook, PostThreadInputModelHook
from .registeruser import (
    RegisterUserHook,
    RegisterUserInputHook,
    RegisterUserInputModelHook,
)
from .templatecontext import TemplateContextHook
from .updatemarkupmetadata import UpdateMarkupMetadataHook
from .updatepost import UpdatePostHook
from .userauth import (
    GetAuthUserHook,
    GetUserFromContextHook,
    GetUserFromTokenHook,
    GetUserFromTokenPayloadHook,
)


authenticate_user_hook = AuthenticateUserHook()
close_thread_hook = CloseThreadHook()
close_thread_input_hook = CloseThreadInputHook()
close_thread_input_model_hook = CloseThreadInputModelHook()
close_threads_hook = CloseThreadsHook()
close_threads_input_hook = CloseThreadsInputHook()
close_threads_input_model_hook = CloseThreadsInputModelHook()
convert_block_ast_to_rich_text_hook = ConvertBlockAstToRichTextHook()
convert_inline_ast_to_text_hook = ConvertInlineAstToTextHook()
create_markdown_hook = CreateMarkdownHook()
create_post_hook = CreatePostHook()
create_thread_hook = CreateThreadHook()
create_user_hook = CreateUserHook()
create_user_token_hook = CreateUserTokenHook()
create_user_token_payload_hook = CreateUserTokenPayloadHook()
delete_thread_hook = DeleteThreadHook()
delete_thread_input_hook = DeleteThreadInputHook()
delete_thread_input_model_hook = DeleteThreadInputModelHook()
delete_thread_post_hook = DeleteThreadPostHook()
delete_thread_post_input_model_hook = DeleteThreadPostInputModelHook()
delete_thread_post_input_post_hook = DeleteThreadPostInputPostHook()
delete_thread_post_input_thread_hook = DeleteThreadPostInputThreadHook()
delete_thread_posts_hook = DeleteThreadPostsHook()
delete_thread_posts_input_model_hook = DeleteThreadPostsInputModelHook()
delete_thread_posts_input_posts_hook = DeleteThreadPostsInputPostsHook()
delete_thread_posts_input_thread_hook = DeleteThreadPostsInputThreadHook()
delete_threads_hook = DeleteThreadsHook()
delete_threads_input_hook = DeleteThreadsInputHook()
delete_threads_input_model_hook = DeleteThreadsInputModelHook()
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
graphql_admin_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_admin_type_defs_hook: List[str] = []
graphql_admin_types_hook: List[SchemaBindable] = []
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
jinja2_extensions_hook: List[Any] = []
jinja2_filters_hook: Dict[str, Any] = {}
move_thread_hook = MoveThreadHook()
move_thread_input_hook = MoveThreadInputHook()
move_thread_input_model_hook = MoveThreadInputModelHook()
move_threads_hook = MoveThreadsHook()
move_threads_input_hook = MoveThreadsInputHook()
move_threads_input_model_hook = MoveThreadsInputModelHook()
parse_markup_hook = ParseMarkupHook()
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
update_markup_metadata_hook = UpdateMarkupMetadataHook()
update_post_hook = UpdatePostHook()
