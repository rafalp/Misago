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
from .deletecategoriescontents import DeleteCategoriesContentsHook
from .filter import FilterHook
from .graphqlcontext import GraphQLContextHook
from .markdown import MarkdownHook
from .movecategoriescontents import MoveCategoriesContentsHook
from .parsemarkup import ParseMarkupHook
from .updatemarkupmetadata import UpdateMarkupMetadataHook
from .updatepost import UpdatePostHook

graphql_admin_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_admin_type_defs_hook: List[str] = []
graphql_admin_types_hook: List[SchemaBindable] = []
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
