from sqlalchemy.sql import ClauseElement

from .querystate import QueryState


def slice_query(state: QueryState, query: ClauseElement) -> ClauseElement:
    if state.offset:
        query = query.offset(state.offset)
    if state.limit:
        query = query.limit(state.limit)
    return query
