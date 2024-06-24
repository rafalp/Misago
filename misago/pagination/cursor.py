from dataclasses import dataclass
from typing import Any, List

from django.http import Http404


class PaginationError(Http404):
    pass


@dataclass
class CursorPaginationResult:
    items: List[Any]
    has_next: bool
    has_previous: bool
    next_cursor: Any | None
    previous_cursor: Any | None


def paginate_queryset(
    request,
    queryset,
    per_page: int,
    order_by: str,
    raise_404: bool = False,
) -> CursorPaginationResult:
    cursor = get_query_value(request, "cursor")
    queryset = queryset.order_by(order_by)
    order_desc = order_by[0] == "-"
    col_name = order_by.lstrip("-")

    if cursor:
        if order_desc:
            filter_kwarg = {f"{col_name}__lt": cursor}
        else:
            filter_kwarg = {f"{col_name}__gt": cursor}
        items_queryset = queryset.filter(**filter_kwarg)
    else:
        items_queryset = queryset

    items = list(items_queryset[: per_page + 1])
    has_next = False
    has_previous = False
    next_cursor = None
    previous_cursor = None

    if cursor and not items and raise_404:
        raise Http404()

    if len(items) > per_page:
        has_next = True
        items = items[:per_page]
        next_cursor = getattr(items[-1], col_name)

    if items:
        cursor = getattr(items[0], col_name)
        if order_desc:
            filter_kwarg = {f"{col_name}__gt": cursor}
        else:
            filter_kwarg = {f"{col_name}__lt": cursor}
        previous_items = list(
            queryset.filter(**filter_kwarg)
            .select_related(None)
            .prefetch_related(None)
            .order_by(col_name)
            .values_list(col_name, flat=True)[: per_page + 1]
        )
        has_previous = bool(previous_items)
        if len(previous_items) > per_page:
            previous_cursor = previous_items[-1]

    return CursorPaginationResult(
        items=items,
        has_next=has_next,
        has_previous=has_previous,
        next_cursor=next_cursor,
        previous_cursor=previous_cursor,
    )


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
