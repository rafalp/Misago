import os

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from ..template import render
from .hooks import exception_handlers_hook

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERROR_500_TEMPLATE_PATH = os.path.join(
    BASE_PATH, "template", "templates", "error_500.html"
)

with open(ERROR_500_TEMPLATE_PATH, "r") as fp:
    ERROR_500_TEMPLATE = fp.read()


class HTTPNotFound(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(404, detail)


async def not_found_route(request: Request, exc: HTTPException):
    return await render(request, "error_404.html", status_code=exc.status_code)


async def server_error_route(request: Request, exc: Exception):
    return HTMLResponse(ERROR_500_TEMPLATE, status_code=500)


def get_exception_handlers():
    exception_handlers_hook.call_action(get_default_exception_handlers)


def get_default_exception_handlers():
    return {
        404: not_found_route,
        500: server_error_route,
    }
