from typing import cast

from sqlalchemy.sql import ColumnElement, TableClause

from .querystate import QueryState


def get_column(
    state: QueryState,
    name: str,
    in_join: bool = False,
) -> ColumnElement:
    if "." not in name:
        if in_join:
            return cast(dict, cast(TableClause, state.join_root).c)[name]
        return state.table.c[name]

    join_name, name = name.rsplit(".", 1)
    return cast(TableClause, state.join_tables)[join_name].c[name]
