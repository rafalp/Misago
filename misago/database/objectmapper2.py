# WIP: Experimental rewrite for object mapper
from dataclasses import dataclass, replace
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Type, Union

from sqlalchemy import asc, desc, func
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
        state = ObjectMapperQueryState(table.alias("m"), table_org_name=table.name)
        return ObjectMapperRootQuery(self, state)


@dataclass
class ObjectMapperJoin:
    left_column: ColumnElement
    right_column: ColumnElement
    table: TableClause
    table_org_name: str
    on_expression: ClauseElement
    include_in_result: bool


@dataclass
class ObjectMapperQueryState:
    table: TableClause
    table_org_name: str
    filter: Optional[List[dict]] = None
    exclude: Optional[List[dict]] = None
    join: Optional[Dict[str, ObjectMapperJoin]] = None
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
        new_join = self.state.join.copy() if self.state.join else {}
        table = self.state.table
        path = []

        for i, column in enumerate(columns):
            if column not in table.c:
                raise InvalidColumnError(column, table)

            path.append(column)
            join_name = ".".join(path)
            if join_name in new_join and i + 1 == columns_len:
                new_join[join_name].include_in_result = True
                continue

            column_obj = table.c[column]
            foreign_key, *_ = column_obj.foreign_keys
            join_table = foreign_key.column.table.alias(f"j{len(new_join)}")
            join_column = join_table.c[foreign_key.column.name]

            new_join[join_name] = ObjectMapperJoin(
                left_column=column_obj,
                right_column=join_column,
                table=join_table,
                table_org_name=foreign_key.column.table.name,
                on_expression=table.c[column] == join_column,
                include_in_result=i + 1 == columns_len,
            )
            table = join_table

        new_state = replace(self.state, join=new_join)
        return ObjectMapperQuery(self.orm, new_state)

    def _join_on_column_simple(self, column: str) -> "ObjectMapperQuery":
        if column not in self.state.table.c:
            raise InvalidColumnError(column, self.state.table)

        new_join = self.state.join.copy() if self.state.join else {}
        if column in new_join:
            new_join[column].include_in_result = True
            new_state = replace(self.state, join=new_join)
            return ObjectMapperQuery(self.orm, new_state)

        column_obj = self.state.table.c[column]
        foreign_key, *_ = column_obj.foreign_keys
        join_table = foreign_key.column.table.alias(f"j{len(new_join)}")
        join_column = join_table.c[foreign_key.column.name]

        new_join[column] = ObjectMapperJoin(
            left_column=column_obj,
            right_column=join_column,
            table=join_table,
            table_org_name=foreign_key.column.table.name,
            on_expression=self.state.table.c[column] == join_column,
            include_in_result=True,
        )
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

    async def all(self, *columns: str, named: bool = True):
        has_joins, rows = await select_rows(self.state, columns)
        if not has_joins:
            return self._all_simple(rows, columns, named)
        return self._all_with_joins(rows, columns, named)

    def _all_simple(self, rows: List[dict], columns: List[str], named: bool):
        if columns:
            if named:
                return [dict(**row) for row in rows]
            else:
                return [tuple(row.values()) for row in rows]

        if named:
            mapping = self.orm.mappings.get(self.state.table_org_name, dict)
            return [mapping(**row) for row in rows]
        else:
            return [tuple(row) for row in rows]

    def _all_with_joins(self, rows: List[dict], columns: List[str], named: bool):
        if columns:
            return rows  # rows are already mapped to cols in joined query

        # Map rows dicts to items
        mappings = [self.orm.mappings.get(self.state.table_org_name, dict)]
        for join in self.state.join.values():
            if join.include_in_result:
                mappings.append(self.orm.mappings.get(join.table_org_name, dict))

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
    tables = 0
    if not columns:
        cols = tuple(state.table.c.values())
        cols_mappings = tuple((0, c.name) for c in cols)
    else:
        raise NotImplementedError("TODO!")

    query_from = state.table
    for i, join in enumerate(state.join.values()):
        if join.include_in_result:
            tables += 1
            cols += tuple(c.label(f"j{i}_{c.name}") for c in join.table.c.values())
            cols_mappings += tuple((tables, c.name) for c in join.table.c.values())

        query_from = query_from.outerjoin(join.table, join.on_expression)

    query = select(cols).select_from(query_from)

    query = filter_query(state, query)
    query = slice_query(state, query)
    query = order_query(state, query)

    rows = []
    for row in await database.fetch_all(query):
        tables_data = tuple({} for _ in range(tables + 1))
        for col, value in enumerate(row.values()):
            col_table, col_name = cols_mappings[col]
            tables_data[col_table][col_name] = value
        rows.append(tables_data)

    return rows


def has_joins(state: ObjectMapperQueryState, columns: Sequence[str]) -> bool:
    if state.join:
        return True

    return False


def get_column(state: ObjectMapperQueryState, name: str) -> ColumnElement:
    if "." not in name:
        return state.table.c[name]

    join_name, name = name.rsplit(".", 1)
    return state.join[join_name].table.c[name]


def filter_query(state: ObjectMapperQueryState, query: ClauseElement) -> ClauseElement:
    if state.filter:
        for filter_clause in state.filter:
            if isinstance(filter_clause, dict):
                for filter_col, filter_value in filter_clause.items():
                    if "__" in filter_col:
                        col_name, expression = filter_col.split("__")
                        col = get_column(state, col_name)
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
                        col = get_column(state, filter_col)
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
                        col = get_column(state, col_name)
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
                        col = get_column(state, filter_col)
                        if filter_value is True or filter_value is False:
                            query = query.where(col == (not filter_value))
                        else:
                            query = query.where(col != filter_value)
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
    if not state.order_by:
        return query

    order_by = []
    for ordering in state.order_by:
        if ordering[0] == "-":
            col = get_column(state, ordering[1:])
            order_by.append(desc(col))
        else:
            col = get_column(state, ordering)
            order_by.append(asc(col))

    return query.order_by(*order_by)


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
