from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from .cacheversions import get_cache_versions
from .conf.dynamicsettings import get_dynamic_settings


class MisagoMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        cache_versions = await get_cache_versions()
        settings = await get_dynamic_settings(cache_versions)

        request.state.cache_versions = cache_versions
        request.state.settings = settings
        request.state.context = {"cache_versions": cache_versions, "settings": settings}

        return await call_next(request)
