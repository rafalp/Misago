from time import time

from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.requests import Request

from .cache import cache
from .conf import settings
from .database import database
from .hooks import graphql_context_hook
from .graphql.admin.schema import admin_schema
from .graphql.context import get_graphql_context
from .graphql.public.schema import public_schema
from .middleware import MisagoMiddleware
from .plugins import import_plugins
from .pubsub import broadcast
from .types import GraphQLContext
from .template import render


import_plugins()

app = Starlette(debug=settings.debug)

app.add_event_handler("startup", cache.connect)
app.add_event_handler("shutdown", cache.disconnect)

if not settings.test:
    # In tests test-runner takes care of connecting and disconnecting
    app.add_event_handler("startup", database.connect)
    app.add_event_handler("shutdown", database.disconnect)

    app.add_event_handler("startup", broadcast.connect)
    app.add_event_handler("shutdown", broadcast.disconnect)

app.add_middleware(MisagoMiddleware)


@app.route("/")
async def homepage(request):
    return await render(request, "index.html", {"time": time()})


async def resolve_graphql_context(request: Request) -> GraphQLContext:
    return await graphql_context_hook.call_action(get_graphql_context, request)


graphql = GraphQL(
    public_schema, debug=settings.debug, context_value=resolve_graphql_context
)

app.mount("/graphql/", graphql)
app.add_websocket_route("/graphql/", graphql.websocket_server)

app.mount(
    "/admin/graphql/",
    GraphQL(admin_schema, debug=settings.debug, context_value=resolve_graphql_context),
)
