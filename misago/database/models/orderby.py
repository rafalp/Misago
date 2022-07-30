from sqlalchemy.sql import ClauseElement, asc, desc

from .getcolumn import get_column
from .querystate import QueryState


def order_query(
    state: QueryState,
    query: ClauseElement,
    *,
    in_join: bool = False,
) -> ClauseElement:
    if not state.order_by:
        return query

    order_by = []
    for ordering in state.order_by:
        if ordering[0] == "-":
            col = get_column(state, ordering[1:], in_join)
            order_by.append(desc(col))
        else:
            col = get_column(state, ordering, in_join)
            order_by.append(asc(col))

    return query.order_by(*order_by)
