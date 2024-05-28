from dataclasses import dataclass
from typing import Any, List, Optional

from django.http import Http404


class PaginationError(Http404):
    pass


@dataclass
class CursorPaginationResult:
    items: List[Any]
    has_next: bool
    has_previous: bool
    first_cursor: Optional[Any]
    last_cursor: Optional[Any]


def paginate_queryset(
    request,
    queryset,
    per_page: int,
    order_by: str,
    raise_404: bool = False,
) -> CursorPaginationResult:
    after = get_query_value(request, "after")
    before = get_query_value(request, "before")

    if after and before:
        raise PaginationError(
            {"after": "'after' and 'before' can't be used at same time"}
        )

    queryset = queryset.order_by(order_by)

    if before:
        return paginate_with_before(queryset, before, per_page, order_by, raise_404)

    return paginate_with_after(queryset, after or 0, per_page, order_by, raise_404)


def get_query_value(request, name: str, default: int | None = None) -> int | None:
    value = request.GET[name] if name in request.GET else default
    if value is None:
        return value

    try:
        value = int(value)
        if value < 1:
            raise ValueError()
    except (TypeError, ValueError):
        raise PaginationError({name: "must be a positive integer"})

    return value


def paginate_with_after(
    queryset,
    after: int,
    per_page: int,
    order_by: str,
    raise_404: bool,
) -> CursorPaginationResult:
    order_desc = order_by[0] == "-"
    col_name = order_by.lstrip("-")

    if after:
        if order_desc:
            filter_kwarg = {f"{col_name}__lt": after}
        else:
            filter_kwarg = {f"{col_name}__gt": after}
        items_queryset = queryset.filter(**filter_kwarg)
    else:
        items_queryset = queryset

    items = list(items_queryset[: per_page + 1])
    has_next = False
    has_previous = False

    if after and not items and raise_404:
        raise Http404()

    if len(items) > per_page:
        has_next = True
        items = items[:per_page]

    if items:
        cursor = getattr(items[0], col_name)
        if order_desc:
            filter_kwarg = {f"{col_name}__gt": cursor}
        else:
            filter_kwarg = {f"{col_name}__lt": cursor}
        has_previous = queryset.filter(**filter_kwarg).order_by(col_name).exists()

    return create_pagination_result(
        col_name,
        items,
        has_next,
        has_previous,
    )


def paginate_with_before(
    queryset,
    before: int,
    per_page: int,
    order_by: str,
    raise_404: bool,
) -> CursorPaginationResult:
    order_desc = order_by[0] == "-"
    col_name = order_by.lstrip("-")

    if order_desc:
        filter_kwarg = {f"{col_name}__gt": before}
    else:
        filter_kwarg = {f"{col_name}__lt": before}
    items_queryset = queryset.filter(**filter_kwarg).order_by(
        col_name if order_desc else f"-{col_name}"
    )

    items = list(reversed(items_queryset[: per_page + 1]))
    has_next = False
    has_previous = False

    if not items and raise_404:
        raise Http404()

    if len(items) > per_page:
        items = items[1:]
        has_previous = True

    if items:
        cursor = getattr(items[-1], col_name)
        if order_desc:
            filter_kwarg = {f"{col_name}__lt": cursor}
        else:
            filter_kwarg = {f"{col_name}__gt": cursor}
        has_next = queryset.filter(**filter_kwarg).order_by(col_name).exists()

    return create_pagination_result(
        col_name,
        items,
        has_next,
        has_previous,
    )


def create_pagination_result(
    col_name: str,
    items: List[Any],
    has_next: bool,
    has_previous: bool,
) -> CursorPaginationResult:
    if items:
        first_cursor = getattr(items[0], col_name)
        last_cursor = getattr(items[-1], col_name)
    else:
        first_cursor = None
        last_cursor = None

    return CursorPaginationResult(
        items=items,
        has_next=has_next,
        has_previous=has_previous,
        first_cursor=first_cursor,
        last_cursor=last_cursor,
    )
