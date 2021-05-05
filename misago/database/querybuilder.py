from typing import Any, Dict, Optional, Sequence

from sqlalchemy import asc, desc
from sqlalchemy.sql import ClauseElement, TableClause, not_, or_


class QueryBuilder:
    def __init__(
        self,
        *,
        filters: Optional[list] = None,
        exclude: Optional[list] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[Sequence[str]] = None,
    ):
        self._filters = filters or None
        self._exclude = exclude or None
        self._offset = offset or 0
        self._limit = limit or 0
        self._order_by = order_by or None

    def filter(self, *clauses: ClauseElement, **kwargs: Dict[str, Any]):
        new_clause = (self._filters or []) + list(clauses) + list(kwargs.items())
        return QueryBuilder(
            filters=new_clause,
            exclude=self._exclude,
            offset=self._offset,
            limit=self._limit,
            order_by=self._order_by,
        )

    def exclude(self, *clauses: ClauseElement, **kwargs: Dict[str, Any]):
        new_clause = (self._exclude or []) + list(clauses) + list(kwargs.items())
        return QueryBuilder(
            filters=self._filters,
            exclude=new_clause,
            offset=self._offset,
            limit=self._limit,
            order_by=self._order_by,
        )

    def offset(self, offset: int):
        return QueryBuilder(
            filters=self._filters,
            exclude=self._exclude,
            offset=offset,
            limit=self._limit,
            order_by=self._order_by,
        )

    def get_offset(self) -> int:
        return self._offset

    def limit(self, limit: int):
        return QueryBuilder(
            filters=self._filters,
            exclude=self._exclude,
            offset=self._offset,
            limit=limit,
            order_by=self._order_by,
        )

    def get_limit(self) -> int:
        return self._limit

    def order_by(self, *clauses: str):
        return QueryBuilder(
            filters=self._filters,
            exclude=self._exclude,
            offset=self._limit,
            limit=self._limit,
            order_by=clauses,
        )

    def get_ordering(self) -> Optional[Sequence[str]]:
        return self._order_by

    def apply_to_query(self, table: TableClause, query):
        query = self.filter_query(table, query)
        query = self.slice_query(query)
        query = self.order_query(table, query)
        return query

    def filter_query(self, table: TableClause, query):
        if self._filters:
            for clause in self._filters:
                query = query.where(self.get_where_clause(table, clause))
        if self._exclude:
            for clause in self._exclude:
                query = query.where(self.get_where_not_clause(table, clause))
        return query

    def get_where_clause(self, table: TableClause, clause):
        # pylint: disable=too-many-return-statements
        if isinstance(clause, ClauseElement):
            return clause  # Pass SQL alchemy clauses verbatim

        col_name, value = clause
        if "__" not in col_name:
            if value is None:
                return table.c[col_name].is_(None)

            return table.c[col_name] == value

        col_name, op = col_name.split("__")
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
                return table.c[col_name].is_(None)
            return table.c[col_name].isnot(None)

        raise ValueError(f"Unknown comparator '{op}'")

    def get_where_not_clause(self, table: TableClause, clause):
        # pylint: disable=too-many-return-statements
        if isinstance(clause, ClauseElement):
            return not_(clause)  # Pass SQL alchemy clauses verbatim

        col_name, value = clause
        if "__" not in col_name:
            if value is None:
                return table.c[col_name].isnot(None)

            return or_(table.c[col_name] != value, table.c[col_name].is_(None))

        col_name, op = col_name.split("__")
        if op == "gt":
            return table.c[col_name] <= value
        if op == "gte":
            return table.c[col_name] < value
        if op == "lt":
            return table.c[col_name] >= value
        if op == "lte":
            return table.c[col_name] > value
        if op == "in":
            return not_(table.c[col_name].in_(value))
        if op == "isnull":
            if value:
                return table.c[col_name].isnot(None)
            return table.c[col_name].is_(None)

        raise ValueError(f"Unknown comparator '{op}'")

    def slice_query(self, query):
        if self._offset:
            query = query.offset(self._offset)
        if self._limit:
            query = query.limit(self._limit)
        return query

    def order_query(self, table: TableClause, query):
        if not self._order_by:
            return query

        order_by = []
        for col_name in self._order_by:
            if col_name[0] == "-":
                order_by.append(desc(table.c[col_name[1:]]))
            else:
                order_by.append(asc(table.c[col_name]))

        return query.order_by(*order_by)
