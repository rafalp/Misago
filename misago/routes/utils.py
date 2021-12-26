from typing import Optional

from starlette.requests import Request

from .exceptions import HTTPNotFound


def get_cursor_or_404(request: Request, query_key: str = "cursor") -> Optional[int]:
    try:
        if request.query_params.get(query_key):
            cursor = int(request.query_params[query_key])
        else:
            cursor = None
    except (TypeError, ValueError):
        raise HTTPNotFound()

    if cursor is not None and cursor < 1:
        raise HTTPNotFound()

    return cursor


def parse_id_or_404(request: Request, path_param: str = "id") -> int:
    try:
        id = request.path_params.get(path_param)
        if id:
            id = int(id)
    except (TypeError, ValueError):
        raise HTTPNotFound()

    if id is None or id < 1:
        raise HTTPNotFound()

    return id
