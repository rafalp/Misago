from starlette.requests import Request

from ..template import render


async def admin_route(request: Request):
    return await render(request, "admin.html")
