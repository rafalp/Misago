from ..types import GraphQLContext, ParseMarkupAction, ParseMarkupFilter, RichText
from .filter import FilterHook


class ParseMarkupHook(FilterHook[ParseMarkupAction, ParseMarkupFilter]):
    async def call_action(
        self, action: ParseMarkupAction, context: GraphQLContext, markup: str,
    ) -> RichText:
        return await self.filter(action, context, markup)
