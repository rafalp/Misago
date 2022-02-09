from typing import Optional

from starlette.requests import Request

from .exceptions import HTTPNotFound


def clean_cursor_or_404(request: Request) -> Optional[int]:
    after = request.query_params.get("after")
    before = request.query_params.get("before")

    try:
        after = int(after) if after is not None else None
        before = int(before) if before is not None else None
    except (TypeError, ValueError) as exception:
        raise HTTPNotFound() from exception

    if (after is not None and after < 1) or (before is not None and before < 1):
        raise HTTPNotFound()

    if after and before:
        raise HTTPNotFound()

    return after, before


def clean_id_or_404(request: Request, path_param: str = "id") -> int:
    try:
        obj_id = request.path_params.get(path_param)
        if obj_id:
            obj_id = int(obj_id)
    except (TypeError, ValueError) as exception:
        raise HTTPNotFound() from exception

    if obj_id is None or obj_id < 1:
        raise HTTPNotFound()

    return obj_id


class ExplicitFirstPage(Exception):
    pass


def clean_page_number_or_404(
    request: Request, path_param: str = "page"
) -> Optional[int]:
    try:
        page = request.path_params.get(path_param)
        if page:
            page = int(page)
    except (TypeError, ValueError) as exception:
        raise HTTPNotFound() from exception

    if page is not None:
        if page < 1:
            raise HTTPNotFound()
        if page == 1:
            raise ExplicitFirstPage()

    return page
