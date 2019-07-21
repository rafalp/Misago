from time import time

from starlette.applications import Starlette
from starlette.responses import JSONResponse


app = Starlette(debug=True)


@app.route('/')
async def homepage(request):
    return JSONResponse({'hello': time()})