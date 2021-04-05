from typing import Iterable, Mapping, Optional, Sequence, Union

from sqlalchemy import asc, desc, func
from sqlalchemy.sql import ClauseElement, TableClause, not_, select

from .database import database


class QueryBuilder:
    def __init__(
        self,
        filters: Optional[list] = None,
        exclude: Optional[list] = None,
        start: Optional[int] = None,
        stop: Optional[int] = None,
        order_by: Optional[Sequence[str]] = None,
    ):
        self._filters = filters or None
        self._exclude = exclude or None
        self._start = start or 0
        self._stop = stop or 0
        self._order_by = order_by or None

    def filter(self, *clauses: Iterable[ClauseElement], **kwargs):
        new_clause = (self._filters or []) + list(clauses) + list(kwargs.items())
        return QueryBuilder(
            new_clause, self._exclude, self._start, self._stop, self._order_by
        )

    def exclude(self, *clauses: Iterable[ClauseElement], **kwargs):
        new_clause = (self._exclude or []) + list(clauses) + list(kwargs.items())
        return QueryBuilder(
            self._filters, new_clause, self._start, self._stop, self._order_by
        )

    def start(self, start: int):
        if self._start:
            raise ValueError("Query is already sliced!")

        return QueryBuilder(
            self._filters, self._exclude, start, self._stop, self._order_by
        )

    def stop(self, stop: int):
        if self._stop:
            raise ValueError("Query is already sliced!")

        return QueryBuilder(
            self._filters, self._exclude, self._start, stop, self._order_by
        )

    def order_by(self, *clauses: Sequence[str]):
        return QueryBuilder(
            self._filters, self._exclude, self._stop, self._stop, *clauses
        )

    def apply_to_query(self, table, query):
        query = self.filter_query(table, query)
        query = self.slice_query(table, query)
        query = self.order_query(table, query)
        return query

    def filter_query(self, table, query):
        if self._filters:
            for clause in self._filters:
                query = query.where(self.get_where_clause(table, clause))
        if self._exclude:
            for clause in self._exclude:
                query = query.where(not_(self.get_where_clause(table, clause)))
        return query

    def get_where_clause(self, table, clause):
        if isinstance(clause, ClauseElement):
            return clause  # Pass SQL alchemy clauses verbatim

        col_name, value = clause
        if "__" not in col_name:
            if col_name not in table.c:
                raise ValueError(
                    f"Undefined column '{col_name}' on table '{table.name}'"
                )
            return table.c[col_name] == value

        col_name, op = col_name.split("__")
        if col_name not in table.c:
            raise ValueError(f"Undefined column '{col_name}' on table '{table.name}'")

        if op == "gt":
            return table.c[col_name] > value
        if op == "gte":
            return table.c[col_name] >= value
        if op == "lt":
            return table.c[col_name] < value
        if op == "lte":
            return table.c[col_name] <= value
        if op == "in":
            return table.c[col_name].in_(value)
        if op == "isnull":
            if value:
                return table.c[col_name] == None
            return table.c[col_name] != None

        raise ValueError(f"Unknown comparator '{op}'")

    def slice_query(self, table, query):
        if self._start:
            query = query.offset(self._start)
        if self._stop:
            query = query.limit(self._stop - self._start)
        return query

    def order_query(self, table, query):
        if not self._order_by:
            return query

        order_by = []
        for col_name in self._order_by:
            if col_name[0] == "-":
                order_by.append(desc(table.c[col_name[1:]]))
            else:
                order_by.append(asc(table.c[col_name]))

        return query.order_by(*order_by)


class MapperBase:
    def __init__(
        self,
        table: TableClause,
        model: Mapping,
        query_builder: QueryBuilder,
        does_not_exist_exc: "DoesNotExist",
        multiple_objects_exc: "MultipleObjectsReturned",
    ):
        self._table = table
        if len(table.primary_key.columns) == 1:
            self._pk = list(table.primary_key.columns)[0]
        else:
            self._pk = None

        self._model = model
        self._query_builder = query_builder

        self.DoesNotExist = does_not_exist_exc
        self.MultipleObjectsReturned = multiple_objects_exc

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        return self._table.c

    def filter(self, *clauses: Iterable[ClauseElement], **kwargs):
        new_query_builder = self._query_builder.filter(*clauses, **kwargs)
        return MapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def exclude(self, *clauses: Iterable[ClauseElement], **kwargs):
        new_query_builder = self._query_builder.exclude(*clauses, **kwargs)
        return MapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def start(self, offset: int):
        new_query_builder = self._query_builder.start(offset)
        return MapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def length(self, offset: int):
        new_query_builder = self._query_builder.stop(offset)
        return MapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def offset(self, start: int, stop: int):
        new_query_builder = self._query_builder.start(start).stop(stop)
        return MapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def order_by(self, *clauses: Sequence[str]):
        new_query_builder = self._query_builder.order_by(clauses)
        return MapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    async def all(self, *columns: Sequence[str], flat: bool = False):
        if columns:
            query = select(self._table.c[col] for col in columns)
            model = dict
        else:
            query = self._table.select(None)
            model = self._model

        query = self._query_builder.apply_to_query(self._table, query)
        result = await database.fetch_all(query)

        if columns and len(columns) == 1 and flat:
            return [row[columns[0]] for row in result]
        return [model(**row) for row in result]

    async def one(self, *columns: Sequence[str]):
        if columns:
            query = select(self._table.c[col] for col in columns)
            model = dict
        else:
            query = self._table.select(None)
            model = self._model

        query_builder = self._query_builder.stop(2)
        query = query_builder.filter_query(self._table, query)
        results = await database.fetch_all(query)

        if not results:
            raise self.DoesNotExist()
        if len(results) > 1:
            raise self.MultipleObjectsReturned()

        return model(**results[0])

    async def count(self) -> int:
        query = select([func.count()]).select_from(self._table)
        query = self._query_builder.filter_query(self._table, query)
        query = self._query_builder.slice_query(self._table, query)
        return await database.fetch_val(query)

    async def update(self, **values) -> int:
        query = self._table.update(None).values(values)
        query = self._query_builder.filter_query(self._table, query)
        query = self._query_builder.slice_query(self._table, query)
        return await database.execute(query)


class Mapper(MapperBase):
    def __init__(self, table: TableClause, model: Mapping = dict):
        self.DoesNotExist = type(
            "%sDoesNotExist" % table.name.title(),
            (DoesNotExist,),
            {},
        )
        self.MultipleObjectsReturned = type(
            "%sMultipleObjectsReturned" % table.name.title(),
            (MultipleObjectsReturned,),
            {},
        )

        super().__init__(
            table,
            model,
            QueryBuilder(),
            self.DoesNotExist,
            self.MultipleObjectsReturned,
        )

    async def insert(self, **values):
        query = self._table.insert(None).values(**values)
        new_row_id = await database.execute(query)
        if self._pk is not None and new_row_id:
            values[self._pk.name] = new_row_id
        return self._model(**values)

    async def all(self, *columns: Sequence[str], flat: bool = False):
        if columns:
            query = select(self._table.c[col] for col in columns)
            model = dict
        else:
            query = self._table.select(None)
            model = self._model

        result = await database.fetch_all(query)

        if columns and len(columns) == 1 and flat:
            return [row[columns[0]] for row in result]
        return [model(**row) for row in result]

    async def delete_all(self, *columns: Sequence[str]) -> int:
        return await database.execute(self._table.delete())


class MapperQuery(MapperBase):
    def __init__(
        self,
        table: TableClause,
        *,
        model: Mapping,
        query_builder: QueryBuilder,
        does_not_exist_exc: "DoesNotExist",
        multiple_objects_exc: "MultipleObjectsReturned",
    ):
        super().__init__(
            table, model, query_builder, does_not_exist_exc, multiple_objects_exc
        )

    async def delete(self):
        query = self._table.delete()
        query = self._query_builder.filter_query(self._table, query)
        return await database.execute(query)


class MultipleObjectsReturned(RuntimeError):
    pass


class DoesNotExist(RuntimeError):
    pass
