from ariadne.asgi import GraphQL

from ..conf import settings
from .admin.schema import admin_schema
from .context import resolve_admin_graphql_context, resolve_public_graphql_context
from .public.schema import public_schema

public_graphql = GraphQL(
    public_schema,
    debug=settings.debug,
    context_value=resolve_public_graphql_context,
)

admin_grapqhl = GraphQL(
    admin_schema,
    debug=settings.debug,
    context_value=resolve_admin_graphql_context,
)
