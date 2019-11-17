from time import time

from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

from .cache import cache
from .conf import settings
from .database import database
from .hooks import graphql_context_hook
from .graphql.schema import schema
from .graphql.context import get_graphql_context
from .plugins import import_plugins
from .types import GraphQLContext


import_plugins()

app = Starlette(debug=settings.debug)

app.add_event_handler("startup", cache.connect)
app.add_event_handler("shutdown", cache.disconnect)

if not settings.test:
    # In tests test-runner takes care of connecting and disconnecting
    app.add_event_handler("startup", database.connect)
    app.add_event_handler("shutdown", database.disconnect)


@app.route("/")
async def homepage(request):
    return JSONResponse({"time": time(), "debug": settings.debug})


async def resolve_graphql_context(request: Request) -> GraphQLContext:
    return await graphql_context_hook.call_action(get_graphql_context, request, {})


graphql_app = GraphQL(
    schema, debug=settings.debug, context_value=resolve_graphql_context
)
app.mount("/graphql/", graphql_app)
