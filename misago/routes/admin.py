from starlette.requests import Request

from ..conf import settings
from ..template import render


async def admin_route(request: Request):
    return await render(request, "admin.html", {"admin_path": settings.admin_path})
