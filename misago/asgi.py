import os
from time import time

from starlette.applications import Starlette
from starlette.responses import JSONResponse

from .conf import settings

settings.setup(os.environ.get("MISAGO_SETTINGS_MODULE"))

app = Starlette(debug=settings.DEBUG)


@app.route("/")
async def homepage(request):
    return JSONResponse({"hello": time()})
