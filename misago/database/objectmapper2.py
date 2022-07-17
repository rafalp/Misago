# WIP: Experimental rewrite for object mapper
from dataclasses import dataclass, replace
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Type, Union

from sqlalchemy import func
from sqlalchemy.sql import ClauseElement, ColumnElement, TableClause, select

from .database import database


class ObjectMapper:
    tables: Dict[str, TableClause]
    mappings: Dict[str, Union[Type, dict]]

    def __init__(self):
        self.tables = {}
        self.mappings = {}

    def set_mapping(self, table: TableClause, repr: Union[Type, dict]):
        self.tables[table.name] = table
        self.mappings[table.name] = repr

    def query_table(self, table: TableClause) -> "ObjectMapperQuery":
        state = ObjectMapperQueryState(table)
        return ObjectMapperQuery(self, state)


@dataclass
class ObjectMapperQueryState:
    table: TableClause
    filter: Optional[List[dict]] = None
    exclude: Optional[List[dict]] = None
    join: Optional[List[Tuple[str, ColumnElement]]] = None
    order_by: Optional[Sequence[str]] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class ObjectMapperQuery:
    orm: ObjectMapper
    state: ObjectMapperQueryState

    def __init__(self, orm: ObjectMapper, state: ObjectMapperQueryState):
        self.orm = orm
        self.state = state

    def join_on(self, *columns: str) -> "ObjectMapperQuery":
        query = self
        for column in columns:
            query = query.join_on_column(column)
        return query

    def join_on_column(self, column: str) -> "ObjectMapperQuery":
        relation, *_ = self.state.table.c[column].foreign_keys
        new_join = (self.state.join or []) + [(column, relation.column)]
        new_state = replace(self.state, join=new_join)
        return ObjectMapperQuery(self.orm, new_state)

    def offset(self, offset: int) -> "ObjectMapperQuery":
        new_state = replace(self.state, offset=offset)
        return ObjectMapperQuery(self.orm, new_state)

    def limit(self, limit: int) -> "ObjectMapperQuery":
        new_state = replace(self.state, limit=limit)
        return ObjectMapperQuery(self.orm, new_state)

    def order_by(self, *columns: str) -> "ObjectMapperQuery":
        new_state = replace(self.state, order_by=columns)
        return ObjectMapperQuery(self.orm, new_state)

    async def all(self, *columns: str):
        has_joins, rows = await select_rows(self.state, columns)
        if not has_joins:
            return self._all_simple(rows, columns)
        return self._all_with_joins(rows, columns)

    def _all_simple(self, rows: List[dict], columns: List[str]):
        if columns:
            return [dict(**row) for row in rows]

        mapping = self.orm.mappings.get(self.state.table.name, dict)
        return [mapping(**row) for row in rows]

    def _all_with_joins(self, rows: List[dict], columns: List[str]):
        if columns:
            return rows  # rows are already mapped to cols in joined query

        # Map rows dicts to items
        mappings = [self.orm.mappings.get(self.state.table.name, dict)]
        for _, join_column in self.state.join:
            mappings.append(self.orm.mappings.get(join_column.table.name, dict))

        for i, row in enumerate(rows):
            rows[i] = [mapping(**row[m]) for m, mapping in enumerate(mappings)]

        return rows

    async def one(self, *columns: str):
        new_state = replace(self.state, offset=None, limit=2)
        results = await select_rows(new_state, columns)
        raise NotImplemented("TODO!")

    async def update(self, values: dict):
        pass

    async def delete(self) -> int:
        pass

    async def count(self) -> int:
        query = select([func.count()]).select_from(self.state.table)
        query = filter_query(self.state, query)
        query = slice_query(self.state, query)
        return await database.fetch_val(query)

    async def exists(self) -> bool:
        new_state = replace(
            self.state,
            limit=self.state.offset + 1 if self.state.offset else 1,
        )
        query = select([func.count()]).select_from(new_state.table)
        query = filter_query(new_state, query)
        query = slice_query(new_state, query)
        return bool(await database.fetch_val(query))


class ObjectMapperRootQuery(ObjectMapperQuery):
    async def insert(self):
        raise NotImplemented("TODO!")

    async def bulk_insert(self):
        raise NotImplemented("TODO!")

    async def delete_all(self) -> int:
        return await database.execute(self.state.table.delete())


async def select_rows(state: ObjectMapperQueryState, columns: Sequence[str]):
    if not has_joins(state, columns):
        return False, await select_rows_simple(state, columns)
    return True, await select_rows_joined(state, columns)


async def select_rows_simple(state: ObjectMapperQueryState, columns: Sequence[str]):
    if columns:
        validate_columns(columns, state.table)
        query = select(state.table.c[col] for col in columns)
    else:
        query = state.table.select(None)

    query = filter_query(state, query)
    query = slice_query(state, query)

    return await database.fetch_all(query)


async def select_rows_joined(state: ObjectMapperQueryState, columns: Sequence[str]):
    cols = list(state.table.c.values())
    cols_tables = [0] * len(cols)
    joins = 0

    query = state.table
    for join_by, foreign_key in state.join:
        joins += 1
        cols += list(foreign_key.table.c.values())
        cols_tables += [joins] * len(foreign_key.table.c)
        query = query.outerjoin(
            foreign_key.table, state.table.c[join_by] == foreign_key
        )

    query = select(*cols).select_from(query)
    rows = []
    for row in await database.fetch_all(query):
        tables_data = {i: {} for i in range(joins + 1)}
        for col, value in enumerate(row.values()):
            tables_data[cols_tables[col]][cols[col].name] = value
        rows.append(list(tables_data.values()))

    return rows


def has_joins(state: ObjectMapperQueryState, columns: Sequence[str]) -> bool:
    if state.join:
        return True

    return False


def filter_query(state: ObjectMapperQueryState, query: ClauseElement) -> ClauseElement:
    return query


def slice_query(state: ObjectMapperQueryState, query: ClauseElement) -> ClauseElement:
    if state.offset:
        query = query.offset(state.offset)
    if state.limit:
        query = query.limit(state.limit)
    return query


class MultipleObjectsReturned(RuntimeError):
    pass


class DoesNotExist(RuntimeError):
    pass


class InvalidColumnError(ValueError):
    def __init__(self, col_name: str, table: TableClause):
        valid_columns = ", ".join(table.c.keys())
        msg = (
            f"'{col_name}' is not a valid column for table '{table.name}'. "
            f"Valid columns are: {valid_columns}"
        )
        super().__init__(msg)


def validate_columns(columns: Iterable[str], table: TableClause):
    for col_name in columns:
        if col_name not in table.c:
            raise InvalidColumnError(col_name, table)


def validate_column(col_name: str, table: TableClause):
    if col_name not in table.c:
        raise InvalidColumnError(col_name, table)
