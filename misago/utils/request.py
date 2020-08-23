from typing import Optional

from starlette.requests import Request


def get_absolute_url(request: Request, url: Optional[str] = None) -> str:
    base_url = request.base_url
    if url:
        return f"{base_url}{url}"
    return str(base_url)
