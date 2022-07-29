from dataclasses import replace
from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import func
from sqlalchemy.sql import ClauseElement, select

from ..database import database
from .exceptions import DoesNotExist, MultipleObjectsReturned
from .filter import filter_query
from .querystate import QueryState
from .select import (
    get_select_join_query,
    select_from_one_table,
    select_with_joins,
    select_with_joins_anonymous_columns,
    select_with_joins_named_columns,
)
from .slice import slice_query
from .validators import (
    validate_column,
    validate_columns,
    validate_conditions,
    validate_join,
)

if TYPE_CHECKING:
    from .mapper import ObjectMapper


class Query:
    orm: "ObjectMapper"
    state: QueryState

    def __init__(self, orm: "ObjectMapper", state: QueryState):
        self.orm = orm
        self.state = state

    def filter(self, *expressions, **conditions) -> "Query":
        filters = list(self.state.filter or [])
        if expressions:
            filters.extend(expressions)
        if conditions:
            validate_conditions(self.state, conditions)
            filters.extend([conditions])
        new_state = replace(self.state, filter=filters)
        return Query(self.orm, new_state)

    def exclude(self, *expressions, **conditions) -> "Query":
        excludes = list(self.state.exclude or [])
        if expressions:
            excludes.extend(expressions)
        if conditions:
            validate_conditions(self.state, conditions)
            excludes.extend([conditions])
        new_state = replace(self.state, exclude=excludes)
        return Query(self.orm, new_state)

    def join_on(self, *columns: str) -> "Query":
        if not self.state.join_root:
            self.state = replace(self.state, join_root=self.state.table.alias("r"))

        new_join = self.state.join[:] if self.state.join else []
        new_join_tables = (
            self.state.join_tables.copy() if self.state.join_tables else {}
        )
        for join_on in columns:
            if "." in join_on:
                table = self.state.table
                join_path = []
                for join_col in join_on.split("."):
                    join_path.append(join_col)
                    validate_column(table, join_col)
                    foreign_key, *_ = table.c[join_col].foreign_keys
                    table = foreign_key.column.table
                    join_name = ".".join(join_path)
                    if join_name not in new_join_tables:
                        new_join_tables[join_name] = table.alias(
                            f"j{len(new_join_tables)}"
                        )
            elif join_on not in new_join_tables:
                validate_column(self.state.table, join_on)
                foreign_key, *_ = self.state.table.c[join_on].foreign_keys
                new_join_tables[join_on] = foreign_key.column.table.alias(
                    f"j{len(new_join_tables)}"
                )

            # Join validated column
            new_join.append(join_on)

        new_state = replace(self.state, join=new_join, join_tables=new_join_tables)
        return Query(self.orm, new_state)

    def offset(self, offset: Optional[int]) -> "Query":
        new_state = replace(self.state, offset=offset)
        return Query(self.orm, new_state)

    def limit(self, limit: Optional[int]) -> "Query":
        new_state = replace(self.state, limit=limit)
        return Query(self.orm, new_state)

    def order_by(self, *columns: str) -> "Query":
        new_state = replace(self.state, order_by=columns or None)
        return Query(self.orm, new_state)

    async def update(self, values: dict):
        validate_columns(self.state.table, values.keys())
        query = self.state.table.update(None).values(values)
        query = filter_query(self.state, query)
        return await database.execute(query)

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
        if self.state.join:
            query = get_select_join_query(self.state, [func.count()], ordered=False)
        else:
            query = select([func.count()]).select_from(self.state.table)
            query = filter_query(self.state, query)
            query = slice_query(self.state, query)
        return await database.fetch_val(query)

    async def exists(self) -> bool:
        query = self.limit(1)
        return bool(await query.count())

    async def one(self, *columns: str, named: bool = False, **filters: str):
        query = self.offset(None).limit(2)
        if filters:
            query = query.filter(**filters)

        results = await query.all(*columns, named=named)
        if not results:
            raise DoesNotExist()
        if len(results) > 1:
            raise MultipleObjectsReturned()

        return results[0]

    async def batch(
        self,
        *columns: str,
        cursor_column: str = "id",
        step_size: int = 20,
        ascending: bool = False,
    ):
        cursor = None
        cursor_clause = cursor_column + ("__gt" if ascending else "__lt")

        base_query = (
            self.order_by(cursor_column if ascending else "-" + cursor_column)
            .offset(0)
            .limit(step_size + 1)
        )

        loop = True
        while loop:
            if cursor:
                query = query.filter(**{cursor_clause: cursor})
            else:
                query = base_query

            results = list(await query.all(*columns))
            if len(results) > step_size:
                results = results[:step_size]
                last_result = results[-1]
                if isinstance(last_result, dict):
                    cursor = last_result[cursor_column]
                else:
                    cursor = getattr(last_result, cursor_column)
            else:
                loop = False

            for result in results:
                yield result

    async def all(self, *columns: str, named: bool = False) -> List[Any]:
        if not self.state.join:
            return await select_from_one_table(
                self.orm,
                self.state,
                columns,
                named=named,
            )

        if columns:
            if named:
                return await select_with_joins_named_columns(self.state, columns)

            return await select_with_joins_anonymous_columns(self.state, columns)

        return await select_with_joins(self.orm, self.state)

    def subquery(self, return_column: Optional[str] = None) -> ClauseElement:
        if return_column:
            if "." in return_column:
                join_name, column = return_column.rsplit(".", 1)
                validate_join(self.state, join_name)
                validate_column(self.state.join_tables[join_name], column)
            else:
                validate_column(self.state.table, return_column)
        else:
            if self.state.join:
                return_column = self.state.join_root.primary_key.columns[0].name
            else:
                return_column = self.state.table.primary_key.columns[0].name

        new_state = replace(self.state, subquery=return_column)
        return Query(self.orm, new_state)

    def as_select_expression(self):
        subquery = self.state.subquery
        if self.state.join:
            if "." in subquery:
                join_name, column = subquery.rsplit(".", 1)
                return get_select_join_query(
                    self.state,
                    [self.state.join_tables[join_name].c[column]],
                    ordered=False,
                )

            return get_select_join_query(
                self.state,
                [self.state.join_root.c[subquery]],
                ordered=False,
            )

        query = select(self.state.table.c[subquery])
        query = filter_query(self.state, query)
        query = slice_query(self.state, query)
        return query


class RootQuery(Query):
    async def insert(self, values: dict):
        table = self.state.table
        validate_columns(table, values.keys())

        query = table.insert(None).values(**values)
        new_row_id = await database.execute(query)
        if table.primary_key.columns is not None and new_row_id:
            values[table.primary_key.columns[0].name] = new_row_id

        mapping = self.orm.mappings.get(table.name, dict)
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
