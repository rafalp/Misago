from typing import Any, Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor

from .action import ActionHook
from .convertblockasttorichtext import ConvertBlockAstToRichTextHook
from .convertinlineasttotext import ConvertInlineAstToTextHook
from .convertrichtextblocktohtml import ConvertRichTextBlockToHTMLHook
from .convertrichtexttohtml import ConvertRichTextToHTMLHook
from .createmarkdown import CreateMarkdownHook
from .createpost import CreatePostHook
from .createthread import CreateThreadHook
from .createuser import CreateUserHook
from .deletecategoriescontents import DeleteCategoriesContentsHook
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
from .markdown import MarkdownHook
from .movecategoriescontents import MoveCategoriesContentsHook
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
from .updatemarkupmetadata import UpdateMarkupMetadataHook
from .updatepost import UpdatePostHook

graphql_admin_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_admin_type_defs_hook: List[str] = []
graphql_admin_types_hook: List[SchemaBindable] = []
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
