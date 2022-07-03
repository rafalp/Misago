from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from sqlalchemy import BigInteger, Integer, SmallInteger

from ...context import Context
from ...database import ObjectMapperQuery


DB_INT_COLUMN = (BigInteger, Integer, SmallInteger)


class Connection:
    default_sort: str = "id"

    async def resolve(
        self,
        context: Context,
        query: ObjectMapperQuery,
        data: dict,
        limit: int,
    ) -> "ConnectionResult":
        sort_by = data.get("sort_by") or self.default_sort
        sorted_query = self.sort_query(query, sort_by)

        nodes, has_previous, has_next = await self.slice_query(
            sorted_query, data, sort_by, limit
        )

        cursor_name = sort_by.lstrip("-")
        edges = self.create_edges(context, nodes, cursor_name, data)

        return ConnectionResult(
            query=query,
            edges=edges,
            has_previous_page=has_previous,
            has_next_page=has_next,
            start_cursor=edges[0].cursor if edges else None,
            end_cursor=edges[-1].cursor if edges else None,
        )

    def sort_query(
        self,
        query: ObjectMapperQuery,
        sort_by: str,
    ) -> Tuple[ObjectMapperQuery, str]:
        return query.order_by(sort_by)

    async def slice_query(
        self, query: ObjectMapperQuery, data: dict, sort_by: str, limit: int
    ) -> Tuple[list, Optional[bool], Optional[bool]]:
        col_name = sort_by.lstrip("-")
        first, last = clean_first_last(data, limit)
        after, before = clean_after_before_number(
            query.table.c[col_name].type, data.get("after"), data.get("before")
        )

        if after:
            if sort_by[0] == "-":
                sliced_query = query.filter(**{f"{col_name}__lt": after})
                opposite_query = query.filter(**{f"{col_name}__gte": after})
            else:
                sliced_query = query.filter(**{f"{col_name}__gt": after})
                opposite_query = query.filter(**{f"{col_name}__lte": after})
        elif before:
            if sort_by[0] == "-":
                sliced_query = query.filter(**{f"{col_name}__gt": before})
                opposite_query = query.filter(**{f"{col_name}__lte": before})
            else:
                sliced_query = query.filter(**{f"{col_name}__lt": before})
                opposite_query = query.filter(**{f"{col_name}__gte": before})
        else:
            sliced_query = query
            opposite_query = None

        if last:
            if sort_by[0] == "-":
                sliced_query = sliced_query.order_by(col_name)
            else:
                sliced_query = sliced_query.order_by("-" + col_name)

        slice_size = first or last
        sliced_query = sliced_query.limit(slice_size + 1)

        nodes = await sliced_query.all()
        has_more = len(nodes) > slice_size

        if opposite_query:
            has_prev = bool(await opposite_query.limit(1).count())
        else:
            has_prev = False

        if last:
            nodes.reverse()
            return nodes[slice_size * -1 :], has_more, has_prev

        return nodes[:slice_size], has_prev, has_more

    def create_edges(
        self, context: Context, nodes: list, cursor_name: str, data: dict
    ) -> List["Edge"]:
        return [
            Edge(node=node, cursor=str(getattr(node, cursor_name))) for node in nodes
        ]


def clean_first_last(data: dict, limit=int) -> Tuple[Optional[int], Optional[int]]:
    if not data.get("first") and not data.get("last"):
        raise ValueError("You must provide either 'first' or 'last' argument.")

    first = data.get("first")
    last = data.get("last")

    if first is not None and last is not None:
        raise ValueError("'first' and 'last' arguments can't be used at same time.")

    if first is not None and first < 1:
        raise ValueError("'first' can't be less than 1.")
    if last is not None and last < 1:
        raise ValueError("'last' can't be less than 1.")

    if first and first > limit:
        raise ValueError(f"'first' can't be greater than {limit}.")
    if last and last > limit:
        raise ValueError(f"'last' can't be greater than {limit}.")

    return first, last


def clean_after_before_number(
    db_col, after, before
) -> Tuple[Optional[Any], Optional[Any]]:
    if after is not None and before is not None:
        raise ValueError("'after' and 'before' arguments can't be used at same time.")

    if isinstance(db_col, DB_INT_COLUMN) and (after or before):
        try:
            if after:
                return int(after), None
            if before:
                return None, int(before)
        except (ValueError, TypeError):
            if after is not None:
                raise ValueError("'after' argument must be a number.")
            if before is not None:
                raise ValueError("'before' argument must be a number.")

    return after, before


@dataclass
class ConnectionResult:
    query: ObjectMapperQuery

    edges: List["Edge"]
    has_previous_page: bool
    has_next_page: bool
    start_cursor: Optional[Any]
    end_cursor: Optional[Any]

    @property
    def page_info(self):
        return self


@dataclass
class Edge:
    node: Any
    cursor: str
