from starlette.requests import Request

from .exceptions import server_error_route


async def error_500_route(request: Request):
    """Little view for testing error 500 page in debug."""
    return await server_error_route(request, ValueError("Test Error"))
