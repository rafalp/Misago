from time import time

from starlette.applications import Starlette
from starlette.responses import JSONResponse

from .conf import settings

app = Starlette(debug=settings.DEBUG)


@app.route("/")
async def homepage(request):
    return JSONResponse({time": time(), "debug": settings.DEBUG})
