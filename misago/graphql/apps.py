from ariadne.asgi import GraphQL

from ..conf import settings
from .context import get_admin_graphql_context, get_public_graphql_context
from .schema import create_admin_schema, create_public_schema

admin_graphql = GraphQL(
    create_admin_schema(),
    debug=settings.debug,
    context_value=get_admin_graphql_context,
)

public_graphql = GraphQL(
    create_public_schema(),
    debug=settings.debug,
    context_value=get_public_graphql_context,
)
