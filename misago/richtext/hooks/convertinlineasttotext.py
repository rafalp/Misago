from typing import Optional, Protocol

from ...context import Context
from ...hooks import FilterHook
from ..types import ParsedMarkupMetadata


class ConvertInlineAstToTextAction(Protocol):
    def __call__(
        self,
        context: Context,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[str]:
        ...


class ConvertInlineAstToTextFilter(Protocol):
    def __call__(
        self,
        action: ConvertInlineAstToTextAction,
        context: Context,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[str]:
        ...


class ConvertInlineAstToTextHook(
    FilterHook[ConvertInlineAstToTextAction, ConvertInlineAstToTextFilter]
):
    is_async = False

    def call_action(
        self,
        action: ConvertInlineAstToTextAction,
        context: Context,
        ast: dict,
        metadata: ParsedMarkupMetadata,
    ) -> Optional[str]:
        return self.filter(action, context, ast, metadata)


convert_inline_ast_to_text_hook = ConvertInlineAstToTextHook()
