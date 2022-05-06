from ariadne_graphql_modules import ObjectType, gql
from graphql import GraphQLResolveInfo

from ...richtext import RichText, parse_markup
from .richtext import RichTextScalar


class RichTextQueries(ObjectType):
    __schema__ = gql(
        """
        type Query {
            richText(markup: String!): RichText!
        }
        """
    )
    __aliases__ = {"richText": "rich_text"}
    __requires__ = [RichTextScalar]

    @staticmethod
    async def resolve_rich_text(
        _, info: GraphQLResolveInfo, *, markup: str
    ) -> RichText:
        rich_text, _ = await parse_markup(info.context, markup)
        return rich_text
