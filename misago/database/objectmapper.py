from typing import Any, Dict, Iterable, Type

from sqlalchemy import func
from sqlalchemy.sql import ClauseElement, TableClause, select

from .database import database
from .querybuilder import QueryBuilder


class ObjectMapperBase:
    def __init__(
        self,
        table: TableClause,
        model: Any,
        query_builder: QueryBuilder,
        does_not_exist_exc: Type["DoesNotExist"],
        multiple_objects_exc: Type["MultipleObjectsReturned"],
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
    def model(self):
        return self._model

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        return self._table.c

    def filter(self, *clauses: ClauseElement, **filters):
        self.validate_filters(filters)

        new_query_builder = self._query_builder.filter(*clauses, **filters)
        return ObjectMapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def exclude(self, *clauses: ClauseElement, **filters):
        self.validate_filters(filters)

        new_query_builder = self._query_builder.exclude(*clauses, **filters)
        return ObjectMapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def validate_filters(self, filters: Dict[str, Any]):
        for col_name in filters:
            if "__" in col_name:
                col_name, _ = col_name.split("__", 1)
            validate_column(col_name, self._table)

    def offset(self, offset: int):
        new_query_builder = self._query_builder.offset(offset)
        return ObjectMapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def limit(self, offset: int):
        new_query_builder = self._query_builder.limit(offset)
        return ObjectMapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    def order_by(self, *clauses: str):
        for col_name in clauses:
            if col_name[0] == "-":
                validate_column(col_name[1:], self._table)
            else:
                validate_column(col_name, self._table)

        new_query_builder = self._query_builder.order_by(*clauses)
        return ObjectMapperQuery(
            self._table,
            model=self._model,
            query_builder=new_query_builder,
            does_not_exist_exc=self.DoesNotExist,
            multiple_objects_exc=self.MultipleObjectsReturned,
        )

    async def all(self, *columns: str, flat: bool = False):
        if columns:
            validate_columns(columns, self._table)
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

    async def iterator(self, *columns: str, batch_size: int = 20, asc: bool = False):
        base_query = self.order_by("id" if asc else "-id").offset(0)
        last_id = None
        run = True
        while run:
            query = base_query.limit(batch_size + 1)
            if last_id:
                if asc:
                    query = query.filter(id__gt=last_id)
                else:
                    query = query.filter(id__lt=last_id)

            items = list(await query.all(*columns))
            if len(items) > batch_size:
                items = items[:batch_size]
                last_id = items[-1].id
            else:
                run = False

            for item in items:
                yield item

    async def one(self, *columns: str, **filters):
        if columns:
            validate_columns(columns, self._table)
            query = select(self._table.c[col] for col in columns)
            model = dict
        else:
            query = self._table.select(None)
            model = self._model

        if filters:
            self.validate_filters(filters)
            query_builder = self._query_builder.filter(**filters)
        else:
            query_builder = self._query_builder

        if query_builder.get_limit() != 1:
            query_builder = query_builder.limit(2)

        query = query_builder.apply_to_query(self._table, query)
        results = await database.fetch_all(query)

        if not results:
            raise self.DoesNotExist()
        if len(results) > 1:
            raise self.MultipleObjectsReturned()

        if columns:
            return dict(**results[0])

        return model(**results[0])

    async def exists(self) -> bool:
        query = self.limit(1)
        return bool(await query.count())

    async def count(self) -> int:
        query = select([func.count()]).select_from(self._table)
        query = self._query_builder.filter_query(self._table, query)
        query = self._query_builder.slice_query(query)
        return await database.fetch_val(query)

    async def update(self, **values) -> int:
        validate_columns(values.keys(), self._table)
        query = self._table.update(None).values(values)
        query = self._query_builder.filter_query(self._table, query)
        return await database.execute(query)


class ObjectMapper(ObjectMapperBase):
    def __init__(self, table: TableClause, model: Any = dict):
        self.DoesNotExist = type(
            f"{table.name.title()}DoesNotExist",
            (DoesNotExist,),
            {},
        )
        self.MultipleObjectsReturned = type(
            f"{table.name.title()}MultipleObjectsReturned",
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
        validate_columns(values.keys(), self._table)
        query = self._table.insert(None).values(**values)
        new_row_id = await database.execute(query)
        if self._pk is not None and new_row_id:
            values[self._pk.name] = new_row_id
        return self._model(**values)

    async def all(self, *columns: str, flat: bool = False):
        if columns:
            validate_columns(columns, self._table)
            query = select(self._table.c[col] for col in columns)
            model = dict
        else:
            query = self._table.select(None)
            model = self._model

        result = await database.fetch_all(query)

        if columns and len(columns) == 1 and flat:
            return [row[columns[0]] for row in result]
        return [model(**row) for row in result]

    async def delete_all(self) -> int:
        return await database.execute(self._table.delete())


class ObjectMapperQuery(ObjectMapperBase):
    def __init__(
        self,
        table: TableClause,
        *,
        model: Any,
        query_builder: QueryBuilder,
        does_not_exist_exc: Type["DoesNotExist"],
        multiple_objects_exc: Type["MultipleObjectsReturned"],
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


def validate_columns(columns: Iterable[str], table: TableClause):
    for col_name in columns:
        if col_name not in table.c:
            raise InvalidColumnError(col_name, table)


def validate_column(col_name: str, table: TableClause):
    if col_name not in table.c:
        raise InvalidColumnError(col_name, table)


class InvalidColumnError(ValueError):
    def __init__(self, col_name: str, table: TableClause):
        valid_columns = ", ".join(table.c.keys())
        msg = (
            f"'{col_name}' is not a valid column for table '{table.name}'. "
            f"Valid columns are: {valid_columns}"
        )
        super().__init__(msg)
