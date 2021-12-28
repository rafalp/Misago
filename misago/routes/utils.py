from typing import Optional

from starlette.requests import Request

from .exceptions import HTTPNotFound


def get_cursor_or_404(request: Request, query_key: str = "cursor") -> Optional[int]:
    cursor: Optional[int] = None
    try:
        if request.query_params.get(query_key):
            cursor = int(request.query_params[query_key])
    except (TypeError, ValueError) as exception:
        raise HTTPNotFound() from exception

    if cursor is not None and cursor < 1:
        raise HTTPNotFound()

    return cursor


def parse_id_or_404(request: Request, path_param: str = "id") -> int:
    try:
        obj_id = request.path_params.get(path_param)
        if obj_id:
            obj_id = int(obj_id)
    except (TypeError, ValueError) as exception:
        raise HTTPNotFound() from exception

    if obj_id is None or obj_id < 1:
        raise HTTPNotFound()

    return obj_id


def parse_page_no_or_404(request: Request, path_param: str = "page") -> Optional[int]:
    try:
        page = request.path_params.get(path_param)
        if page:
            page = int(page)
    except (TypeError, ValueError) as exception:
        raise HTTPNotFound() from exception

    if page is not None and page < 1:
        raise HTTPNotFound()

    return page
