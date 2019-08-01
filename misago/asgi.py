import os
from time import time

from starlette.applications import Starlette
from starlette.responses import JSONResponse

from . import setup
from .conf import settings


def get_asgi_application() -> Starlette:
    setup()

    app = Starlette(debug=settings.DEBUG)
    app.router.add_route("/", homepage)

    return app


async def homepage(request):
    return JSONResponse({"hello": time()})
