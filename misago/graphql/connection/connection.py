from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Union, cast

from ...context import Context
from ...database import ObjectMapper, ObjectMapperQuery
from .cleanargs import ValidationError, clean_after_before, clean_first_last


class Connection:
    default_sort: str

    def __init__(self, default_sort: str = "id"):
        self.default_sort = default_sort

    async def resolve(
        self,
        context: Optional[Context],
        query: Union[ObjectMapper, ObjectMapperQuery],
        data: dict,
        limit: int,
    ) -> "ConnectionResult":
        sort_by = data.get("sort_by") or self.default_sort
        nodes, has_previous, has_next = await self.slice_query(
            query, data, sort_by, limit
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

    async def slice_query(
        self,
        query: Union[ObjectMapper, ObjectMapperQuery],
        data: dict,
        sort_by: str,
        limit: int,
    ) -> Tuple[list, bool, bool]:
        col_name = sort_by.lstrip("-")
        first, last = clean_first_last(data, limit)
        after, before = clean_after_before(data, query.table.c[col_name])

        if first is not None and before is not None:
            raise ValidationError(
                "'first' and 'before' arguments can't be used at same time."
            )
        if last is not None and after is not None:
            raise ValidationError(
                "'last' and 'after' arguments can't be used at same time."
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
        else:
            sliced_query = sliced_query.order_by(sort_by)

        slice_size = cast(int, first or last)
        sliced_query = sliced_query.limit(slice_size + 1)

        nodes = await sliced_query.all()
        has_more: bool = len(nodes) > slice_size

        if opposite_query:
            has_prev = bool(await opposite_query.limit(1).count())
        else:
            has_prev = False

        if last:
            nodes.reverse()
            return nodes[slice_size * -1 :], has_more, has_prev

        return nodes[:slice_size], has_prev, has_more

    def create_edges(
        self, context: Optional[Context], nodes: list, cursor_name: str, data: dict
    ) -> List["Edge"]:
        return [
            Edge(node=node, cursor=str(getattr(node, cursor_name))) for node in nodes
        ]


@dataclass
class ConnectionResult:
    query: Union[ObjectMapper, ObjectMapperQuery]

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


connection = Connection()
