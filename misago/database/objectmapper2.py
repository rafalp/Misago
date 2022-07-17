# WIP: Experimental rewrite for object mapper
from dataclasses import dataclass, replace
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Type, Union

from sqlalchemy import func
from sqlalchemy.sql import ClauseElement, ColumnElement, TableClause, not_, select

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
        return ObjectMapperRootQuery(self, state)


@dataclass
class ObjectMapperQueryState:
    table: TableClause
    filter: Optional[List[dict]] = None
    exclude: Optional[List[dict]] = None
    join: Optional[List[Tuple[TableClause, ClauseElement, bool]]] = None
    order_by: Optional[Sequence[str]] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class ObjectMapperQuery:
    orm: ObjectMapper
    state: ObjectMapperQueryState

    def __init__(self, orm: ObjectMapper, state: ObjectMapperQueryState):
        self.orm = orm
        self.state = state

    def filter(self, *expressions, **conditions) -> "ObjectMapperQuery":
        filters = list(self.state.filter or [])
        if expressions:
            filters.extend(expressions)
        if conditions:
            filters.extend([conditions])
        new_state = replace(self.state, filter=filters)
        return ObjectMapperQuery(self.orm, new_state)

    def exclude(self, *expressions, **conditions) -> "ObjectMapperQuery":
        excludes = list(self.state.exclude or [])
        if expressions:
            excludes.extend(expressions)
        if conditions:
            excludes.extend([conditions])
        new_state = replace(self.state, exclude=excludes)
        return ObjectMapperQuery(self.orm, new_state)

    def join_on(self, *columns: str) -> "ObjectMapperQuery":
        query = self
        for column in columns:
            query = query.join_on_column(column)
        return query

    def join_on_column(self, column: str) -> "ObjectMapperQuery":
        if "." in column:
            return self._join_on_column_deep(column.split("."))

        return self._join_on_column_simple(column)

    def _join_on_column_deep(self, columns: Sequence[str]) -> "ObjectMapperQuery":
        columns_len = len(columns)
        new_join = self.state.join or []
        table = self.state.table

        for i, column in enumerate(columns):
            if column not in table.c:
                raise InvalidColumnError(column, table)

            foreign_key, *_ = table.c[column].foreign_keys
            new_join.append(
                (
                    foreign_key.column.table,
                    table.c[column] == foreign_key.column,
                    i + 1 == columns_len,
                )
            )
            table = foreign_key.column.table

        new_state = replace(self.state, join=new_join)
        return ObjectMapperQuery(self.orm, new_state)

    def _join_on_column_simple(self, column: str) -> "ObjectMapperQuery":
        if column not in self.state.table.c:
            raise InvalidColumnError(column, self.state.table)

        foreign_key, *_ = self.state.table.c[column].foreign_keys
        new_join = (self.state.join or []) + [
            (
                foreign_key.column.table,
                self.state.table.c[column] == foreign_key.column,
                True,
            )
        ]
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

    async def update(self, values: dict):
        raise NotImplementedError("TODO")

    async def delete(self) -> int:
        query = self.state.table.delete()
        query = filter_query(self.state, query)
        await database.execute(query)

    async def delete_all(self) -> int:
        raise NotImplementedError(
            "'delete_all()' method is not available on filtered queries. "
            "To delete filtered objects call 'delete()'."
        )

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
        for join_table, _, include_in_result in self.state.join:
            if include_in_result:
                mappings.append(self.orm.mappings.get(join_table.name, dict))

        for i, row in enumerate(rows):
            rows[i] = (mapping(**row[m]) for m, mapping in enumerate(mappings))

        return rows

    async def one(self, *columns: str):
        new_state = replace(self.state, offset=None, limit=2)
        results = await select_rows(new_state, columns)
        raise NotImplemented("TODO!")


class ObjectMapperRootQuery(ObjectMapperQuery):
    async def insert(self, values: dict):
        validate_columns(values.keys(), self.state.table)
        query = self.state.table.insert(None).values(**values)
        new_row_id = await database.execute(query)
        if self.state.table.primary_key.columns is not None and new_row_id:
            values[self.state.table.primary_key.columns[0].name] = new_row_id

        mapping = self.orm.mappings.get(self.state.table.name, dict)
        return mapping(**values)

    async def bulk_insert(self, values: List[dict]):
        new_memberships = self.state.table.insert().values(values)
        await database.fetch_all(new_memberships)

    async def delete_all(self):
        await database.execute(self.state.table.delete())

    async def delete(self) -> int:
        raise NotImplementedError(
            "'delete()' method is not available on root queries. "
            "To delete all objects call 'delete_all()'."
        )


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
    query = order_query(state, query)

    return await database.fetch_all(query)


async def select_rows_joined(state: ObjectMapperQueryState, columns: Sequence[str]):
    cols = list(state.table.c.values())
    cols_tables = [0] * len(cols)
    joins = 0

    query = state.table
    for join_table, join_clause, include_in_result in state.join:
        if include_in_result:
            joins += 1
            cols += list(join_table.c.values())
            cols_tables += [joins] * len(join_table.c)

        query = query.outerjoin(join_table, join_clause)

    query = select(*cols).select_from(query)

    query = filter_query(state, query)
    query = slice_query(state, query)
    query = order_query(state, query)

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
    if state.filter:
        for filter_clause in state.filter:
            if isinstance(filter_clause, dict):
                for filter_col, filter_value in filter_clause.items():
                    if "__" in filter_col:
                        col_name, expression = filter_col.split("__")
                        col = state.table.c[col_name]
                        if expression == "in":
                            query = query.where(col.in_(filter_value))
                        elif expression == "gte":
                            query = query.where(col >= filter_value)
                        elif expression == "gt":
                            query = query.where(col > filter_value)
                        elif expression == "lte":
                            query = query.where(col <= filter_value)
                        elif expression == "lt":
                            query = query.where(col < filter_value)
                        elif expression == "isnull":
                            if filter_value:
                                query = query.where(col.is_(None))
                            else:
                                query = query.where(col.isnot(None))
                    else:
                        col = state.table.c[filter_col]
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

    if state.exclude:
        for exclude_clause in state.exclude:
            if isinstance(exclude_clause, dict):
                for filter_col, filter_value in exclude_clause.items():
                    if "__" in filter_col:
                        col_name, expression = filter_col.split("__")
                        col = state.table.c[col_name]
                        if expression == "in":
                            query = query.where(not_(col.in_(filter_value)))
                        elif expression == "gte":
                            query = query.where(col < filter_value)
                        elif expression == "gt":
                            query = query.where(col <= filter_value)
                        elif expression == "lte":
                            query = query.where(col > filter_value)
                        elif expression == "lt":
                            query = query.where(col >= filter_value)
                        elif expression == "isnull":
                            if filter_value:
                                query = query.where(col.isnot(None))
                            else:
                                query = query.where(col.is_(None))
                    else:
                        if filter_value is True or filter_value is False:
                            query = query.where(
                                state.table.c[filter_col] == (not filter_value)
                            )
                        else:
                            query = query.where(
                                state.table.c[filter_col] != filter_value
                            )
            else:
                query = query.where(not_(exclude_clause))

    return query


def slice_query(state: ObjectMapperQueryState, query: ClauseElement) -> ClauseElement:
    if state.offset:
        query = query.offset(state.offset)
    if state.limit:
        query = query.limit(state.limit)
    return query


def order_query(state: ObjectMapperQueryState, query: ClauseElement) -> ClauseElement:
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
