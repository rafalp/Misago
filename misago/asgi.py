from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from .cache import cache
from .conf import settings
from .database import database
from .graphql.apps import admin_grapqhl, public_graphql
from .middleware import MisagoMiddleware
from .plugins import import_plugins
from .pubsub import broadcast
from .routes import register_routes

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.mount("/graphql/", public_graphql)
app.add_websocket_route("/graphql/", public_graphql.websocket_server)

app.mount("/admin/graphql/", admin_grapqhl)

register_routes(app)
