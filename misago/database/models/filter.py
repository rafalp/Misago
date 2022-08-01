from typing import Any, Iterable

from sqlalchemy.sql import ClauseElement, ColumnElement, and_, not_, or_

from .getcolumn import get_column
from .querystate import Lookup, QueryState


def filter_query(
    state: QueryState,
    query: ClauseElement,
    *,
    in_join: bool = False,
) -> ClauseElement:
    lookups = []
    or_lookups = []

    if state.filter:
        lookups += get_filter_expressions(state, state.filter, in_join)
    if state.exclude:
        lookups += get_exclude_expressions(state, state.exclude, in_join)
    if state.or_filter:
        for or_filter in state.or_filter:
            or_lookups.append(and_(*get_filter_expressions(state, or_filter, in_join)))
    if state.or_exclude:
        for or_exclude in state.or_exclude:
            or_lookups.append(
                and_(*get_exclude_expressions(state, or_exclude, in_join))
            )

    if or_lookups:
        return query.where(*lookups, or_(*or_lookups))
    if lookups:
        return query.where(*lookups)

    return query


def get_filter_expressions(
    state: QueryState,
    lookups: Iterable[Lookup],
    in_join: bool,
) -> ClauseElement:
    expressions = []
    for lookup in lookups:
        if isinstance(lookup, dict):
            for filter_col, filter_value in lookup.items():
                if "__" in filter_col:
                    col_name, clause = filter_col.split("__")
                    col = get_column(state, col_name, in_join)
                    expressions.append(get_filter_expression(col, clause, filter_value))
                else:
                    col = get_column(state, filter_col, in_join)
                    if filter_value is True:
                        expressions.append(col.is_(True))
                    elif filter_value is False:
                        expressions.append(col.is_(False))
                    elif filter_value is None:
                        expressions.append(col.is_(None))
                    else:
                        expressions.append(col == filter_value)
        else:
            expressions.append(lookup)

    return expressions


def get_filter_expression(
    col: ColumnElement,
    clause: str,
    value: Any,
) -> ClauseElement:
    # pylint: disable=too-many-return-statements
    if clause == "in":
        if hasattr(value, "as_select_expression"):
            return col.in_(value.as_select_expression())
        return col.in_(value)

    if clause == "gte":
        return col >= value
    if clause == "gt":
        return col > value
    if clause == "lte":
        return col <= value
    if clause == "lt":
        return col < value

    if clause == "contains":
        return contains(col, value)
    if clause == "icontains":
        return contains(col, value, case_sensitive=False)

    if clause == "startswith":
        return startswith(col, value)
    if clause == "istartswith":
        return startswith(col, value, case_sensitive=False)

    if clause == "endswith":
        return endswith(col, value)
    if clause == "iendswith":
        return endswith(col, value, case_sensitive=False)

    if clause == "ilike":
        return ilike(col, value)

    if clause == "simplesearch":
        return simplesearch(col, value)
    if clause == "isimplesearch":
        return simplesearch(col, value, case_sensitive=False)

    if clause == "isnull":
        if value:
            return col.is_(None)
        return col.isnot(None)

    raise ValueError(f"Unknown clause '{clause}'")


def get_exclude_expressions(
    state: QueryState,
    lookups: Iterable[Lookup],
    in_join: bool,
) -> ClauseElement:
    expressions = []
    for lookup in lookups:
        if isinstance(lookup, dict):
            for filter_col, filter_value in lookup.items():
                if "__" in filter_col:
                    col_name, clause = filter_col.split("__")
                    col = get_column(state, col_name, in_join)
                    expressions.append(
                        get_exclude_expression(col, clause, filter_value)
                    )
                else:
                    col = get_column(state, filter_col, in_join)
                    if filter_value is True or filter_value is False:
                        expressions.append(col == (not filter_value))
                    elif filter_value is None:
                        expressions.append(col.isnot(None))
                    else:
                        # col != 3 OR col IS NULL
                        expressions.append(or_(col != filter_value, col.is_(None)))
        else:
            expressions.append(not_(lookup))

    return expressions


def get_exclude_expression(
    col: ColumnElement,
    clause: str,
    value: Any,
) -> ClauseElement:
    # pylint: disable=too-many-return-statements
    if clause == "in":
        if hasattr(value, "as_select_expression"):
            return not_(col.in_(value.as_select_expression()))
        return not_(col.in_(value))

    if clause == "gte":
        return col < value
    if clause == "gt":
        return col <= value
    if clause == "lte":
        return col > value
    if clause == "lt":
        return col >= value

    if clause == "isnull":
        if value:
            return col.isnot(None)
        return col.is_(None)

    return not_(get_filter_expression(col, clause, value))


ESCAPE_CHARACTER = "\\"


def simplesearch(
    column: ColumnElement, value: str, case_sensitive: bool = True
) -> ClauseElement:
    start = value.endswith("*")
    end = value.startswith("*")
    value = escape_value(value.strip("*").strip())

    if start and end:
        return contains(column, value, case_sensitive)
    if start:
        return startswith(column, value, case_sensitive)
    if end:
        return endswith(column, value, case_sensitive)

    return match(column, value, case_sensitive)


def contains(
    column: ColumnElement, value: str, case_sensitive: bool = True
) -> ClauseElement:
    value = f"%{escape_value(value)}%"
    return match(column, value, case_sensitive)


def startswith(
    column: ColumnElement, value: str, case_sensitive: bool = True
) -> ClauseElement:
    value = f"{escape_value(value)}%"
    return match(column, value, case_sensitive)


def endswith(
    column: ColumnElement, value: str, case_sensitive: bool = True
) -> ClauseElement:
    value = f"%{escape_value(value)}"
    return match(column, value, case_sensitive)


def match(
    column: ColumnElement, value: str, case_sensitive: bool = True
) -> ClauseElement:
    if case_sensitive:
        return column.like(value, escape=ESCAPE_CHARACTER)
    return column.ilike(value, escape=ESCAPE_CHARACTER)


def ilike(column: ColumnElement, value: str) -> ClauseElement:
    value = escape_value(value)
    return column.ilike(value, escape=ESCAPE_CHARACTER)


def escape_value(value) -> str:
    return (
        value.replace(ESCAPE_CHARACTER, ESCAPE_CHARACTER * 2)
        .replace(r"%", r"\%")
        .replace(r"_", r"\_")
    )
