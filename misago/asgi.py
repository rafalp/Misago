from time import time

from starlette.applications import Starlette
from starlette.responses import JSONResponse

from .conf import settings
from .plugins import import_plugins


import_plugins()

app = Starlette(debug=settings.debug)


@app.route("/")
async def homepage(request):
    return JSONResponse({"time": time(), "debug": settings.debug})
