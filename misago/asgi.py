from time import time

from ariadne.asgi import GraphQL
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from .conf import settings
from .database import database
from .graphql.schema import schema
from .plugins import import_plugins


import_plugins()

app = Starlette(debug=settings.debug)

if not settings.test:
    # In tests test-runner takes care of connecting and disconnecting
    app.add_event_handler("startup", database.connect)
    app.add_event_handler("shutdown", database.disconnect)


@app.route("/")
async def homepage(request):
    return JSONResponse({"time": time(), "debug": settings.debug})


graphql_app = GraphQL(schema, debug=settings.debug)
app.mount("/graphql/", graphql_app)
