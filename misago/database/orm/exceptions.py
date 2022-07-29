from sqlalchemy.sql import TableClause

from .querystate import QueryState


class MultipleObjectsReturned(RuntimeError):
    pass


class DoesNotExist(RuntimeError):
    pass


class InvalidJoinError(LookupError):
    def __init__(self, join_name: str, state: QueryState):
        msg = (
            f"'{join_name}' is not a specified join for query. "
            f"Specified joins: {state.join}"
        )
        super().__init__(msg)


class InvalidColumnError(LookupError):
    def __init__(self, col_name: str, table: TableClause):
        valid_columns = ", ".join(table.c.keys())
        msg = (
            f"'{col_name}' is not a valid column for table '{table.name}'. "
            f"Valid columns are: {valid_columns}"
        )
        super().__init__(msg)
