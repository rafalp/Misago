from dataclasses import dataclass
from typing import Any, List, Optional

from django.http import Http404
from rest_framework.exceptions import ValidationError


class PaginationError(ValidationError):
    pass


@dataclass
class PaginationResult:
    items: List[Any]
    has_next: bool
    has_previous: bool
    first_cursor: Optional[Any]
    last_cursor: Optional[Any]


def paginate_queryset(
    request,
    queryset,
    order_by: str,
    max_limit: int,
    raise_404: bool = False,
) -> PaginationResult:
    after = get_query_value(request, "after")
    before = get_query_value(request, "before")
    limit = get_query_value(request, "limit") or max_limit

    if after and before:
        raise PaginationError(
            {"after": "'after' and 'before' can't be used at same time"}
        )

    if limit > max_limit:
        raise PaginationError({"limit": f"can't be greater than '{max_limit}'"})

    queryset = queryset.order_by(order_by)

    if before:
        return paginate_with_before(queryset, before, order_by, limit, raise_404)

    return paginate_with_after(queryset, after or 0, order_by, limit, raise_404)


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
    order_by: str,
    limit: int,
    raise_404: bool,
) -> PaginationResult:
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

    items = list(items_queryset[: limit + 1])
    has_next = False
    has_previous = False

    if after and not items and raise_404:
        raise Http404()

    if len(items) > limit:
        has_next = True
        items = items[:limit]

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
    order_by: str,
    limit: int,
    raise_404: bool,
) -> PaginationResult:
    order_desc = order_by[0] == "-"
    col_name = order_by.lstrip("-")

    if order_desc:
        filter_kwarg = {f"{col_name}__gt": before}
    else:
        filter_kwarg = {f"{col_name}__lt": before}
    items_queryset = queryset.filter(**filter_kwarg).order_by(
        col_name if order_desc else f"-{col_name}"
    )

    items = list(reversed(items_queryset[: limit + 1]))
    has_next = False
    has_previous = False

    if not items and raise_404:
        raise Http404()

    if len(items) > limit:
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
) -> PaginationResult:
    if items:
        first_cursor = getattr(items[0], col_name)
        last_cursor = getattr(items[-1], col_name)
    else:
        first_cursor = None
        last_cursor = None

    return PaginationResult(
        items=items,
        has_next=has_next,
        has_previous=has_previous,
        first_cursor=first_cursor,
        last_cursor=last_cursor,
    )
