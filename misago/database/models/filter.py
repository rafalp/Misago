from typing import Any, Dict, List, TypeAlias, cast

from sqlalchemy.sql import ClauseElement, ColumnElement, not_, or_

from .getcolumn import get_column
from .querystate import QueryState


def filter_query(
    state: QueryState, query: ClauseElement, *, in_join: bool = False
) -> ClauseElement:
    if state.filter:
        query = apply_filters(state, query, in_join)
    if state.exclude:
        query = apply_excludes(state, query, in_join)

    return query


FilterClause: TypeAlias = ClauseElement | Dict[str, Any]


def apply_filters(
    state: QueryState, query: ClauseElement, in_join: bool
) -> ClauseElement:
    for filter_clause in cast(List[FilterClause], state.filter):
        if isinstance(filter_clause, dict):
            for filter_col, filter_value in filter_clause.items():
                if "__" in filter_col:
                    col_name, clause = filter_col.split("__")
                    col = get_column(state, col_name, in_join)
                    query = query.where(
                        get_filter_expression(col, clause, filter_value)
                    )
                else:
                    col = get_column(state, filter_col, in_join)
                    if filter_value is True:
                        query = query.where(col.is_(True))
                    elif filter_value is False:
                        query = query.where(col.is_(False))
                    elif filter_value is None:
                        query = query.where(col.is_(None))
                    else:
                        query = query.where(col == filter_value)
        else:
            query = query.where(filter_clause)

    return query


def get_filter_expression(col: ColumnElement, clause: str, value: Any) -> ClauseElement:
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


def apply_excludes(
    state: QueryState, query: ClauseElement, in_join: bool
) -> ClauseElement:
    # pylint: disable=too-many-nested-blocks
    for exclude_clause in cast(List[FilterClause], state.exclude):
        if isinstance(exclude_clause, dict):
            for filter_col, filter_value in exclude_clause.items():
                if "__" in filter_col:
                    col_name, clause = filter_col.split("__")
                    col = get_column(state, col_name, in_join)
                    query = query.where(
                        get_exclude_expression(col, clause, filter_value)
                    )
                else:
                    col = get_column(state, filter_col, in_join)
                    if filter_value is True or filter_value is False:
                        query = query.where(col == (not filter_value))
                    elif filter_value is None:
                        query = query.where(col.isnot(None))
                    else:
                        # col != 3 OR col IS NULL
                        query = query.where(or_(col != filter_value, col.is_(None)))
        else:
            query = query.where(not_(exclude_clause))

    return query


def get_exclude_expression(
    col: ColumnElement, clause: str, value: Any
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