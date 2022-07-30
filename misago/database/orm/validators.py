from typing import Any, Dict, Iterable, Sequence, cast

from sqlalchemy.sql import TableClause

from .exceptions import InvalidColumnError, InvalidJoinError
from .querystate import QueryState


def validate_columns(table: TableClause, columns: Iterable[str]):
    for col_name in columns:
        if col_name not in table.c:
            raise InvalidColumnError(col_name, table)


def validate_column(table: TableClause, col_name: str):
    if col_name not in table.c:
        raise InvalidColumnError(col_name, table)


def validate_join(state: QueryState, join_name: str):
    if not state.join or join_name not in cast(dict, state.join_tables):
        raise InvalidJoinError(join_name, state)


def validate_conditions(state: QueryState, conditions: Dict[str, Any]):
    for condition in conditions:
        if "__" in condition:
            condition, _ = condition.split("__", 1)
        if "." in condition:
            join_name, field = condition.rsplit(".", 1)
            validate_join(state, join_name)
            validate_column(cast(dict, state.join_tables)[join_name].element, field)
        else:
            validate_column(state.table, condition)
