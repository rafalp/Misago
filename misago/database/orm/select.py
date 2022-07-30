from collections import namedtuple
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, Tuple, TypeAlias, cast

from databases.interfaces import Record
from sqlalchemy.sql import ClauseElement, ColumnElement, TableClause, select

from ..database import database
from .exceptions import InvalidColumnError
from .filter import filter_query
from .orderby import order_query
from .querystate import QueryState
from .slice import slice_query
from .validators import validate_columns

if TYPE_CHECKING:
    from .mapper import ObjectMapper


# Result's mapping (Model, Dict, Named Tuple)
DBMapping: TypeAlias = Any


async def select_from_one_table(
    orm: "ObjectMapper",
    state: QueryState,
    columns: Sequence[str],
    *,
    named: bool = False,
) -> List[DBMapping]:
    """Select all columns from simple select, return them as dict/tuple/mapping"""
    if columns:
        validate_columns(state.table, columns)
        query = select(state.table.c[col] for col in columns)
    else:
        query = state.table.select(None)

    query = filter_query(state, query)
    query = slice_query(state, query)
    query = order_query(state, query)

    records = await database.fetch_all(query)

    mapping: DBMapping

    if columns:
        if named:
            mapping = namedtuple("Result", columns)  # type: ignore
            return [mapping(**record_dict(record)) for record in records]

        return [record_tuple(record) for record in records]

    mapping = orm.mappings.get(state.table.name, dict)
    return [mapping(**record_dict(record)) for record in records]


# Holds result's columns grouped per table as dicts
TablesData: TypeAlias = Sequence[dict]


async def select_with_joins(
    orm: "ObjectMapper",
    state: QueryState,
) -> List[DBMapping]:
    root = cast(TableClause, state.join_root)
    joins_names = cast(List[str], state.join)
    joins_tables = cast(Dict[str, TableClause], state.join_tables)

    # Build cols tuple and index -> name tuple
    cols = tuple(root.c.values())
    cols_mappings = tuple((0, c.name) for c in cols)

    for i, join_name in enumerate(joins_names, 1):
        join_table = joins_tables[join_name]
        cols += tuple(c.label(f"t{i}_{c.name}") for c in join_table.c.values())
        cols_mappings += tuple((i, c.name) for c in join_table.c.values())

    # Build SELECT ... FROM ... JOIN ... query
    query = get_select_join_query(state, cols)

    # Build tuples with primary key names and mappings
    keys: Tuple[str, ...] = (root.primary_key[0].name,)
    mappings: Tuple[DBMapping, ...] = (orm.mappings.get(state.table.name, dict),)

    for join_on in joins_names:
        join_table = joins_tables[join_on]
        keys += (join_table.primary_key[0].name,)
        mappings += (orm.mappings.get(join_table.element.name, dict),)

    # Fetch results and convert them to models
    types_count = 1 + len(joins_names)
    results = []

    for record in await database.fetch_all(query):
        tables_data: TablesData = tuple({} for _ in range(types_count))
        for col, value in enumerate(record_tuple(record)):
            col_table, col_name = cols_mappings[col]
            tables_data[col_table][col_name] = value

        results.append(
            tuple(
                mappings[i](**data) if data[keys[i]] is not None else None
                for i, data in enumerate(tables_data)
            )
        )

    return results


async def select_with_joins_named_columns(
    state: QueryState,
    columns: Sequence[str],
) -> List[DBMapping]:
    root = cast(TableClause, state.join_root)
    joins_names = cast(List[str], state.join)
    joins_tables = cast(Dict[str, TableClause], state.join_tables)

    # Build cols tuple and index -> name tuple
    cols: Tuple[ColumnElement, ...] = tuple()
    cols_mappings: Tuple[Tuple[int, str], ...] = tuple()
    skip_columns: Tuple[
        str | None, ...
    ] = tuple()  # Columns we need to remove from result set

    pk = root.primary_key[0]
    if pk.name not in columns:
        cols += (pk,)
        cols_mappings += ((0, pk.name),)
        skip_columns += (pk.name,)
    else:
        skip_columns += (None,)

    for i, join_name in enumerate(joins_names, 1):
        join_table = joins_tables[join_name]
        join_pk = join_table.primary_key[0]
        if f"{join_name}.{join_pk.name}" not in columns:
            cols += (join_pk,)
            cols_mappings += ((i, join_pk.name),)
            skip_columns += (join_pk.name,)
        else:
            skip_columns += (None,)

    joins_index = {join_on: i for i, join_on in enumerate(joins_names, 1)}
    for i, column in enumerate(columns):
        if "." not in column:
            try:
                col = root.c[column]
                cols += (col,)
                cols_mappings += ((0, col.name),)
            except KeyError as error:
                raise InvalidColumnError(column, state.table) from error
        else:
            join_name, column = column.rsplit(".", 1)
            try:
                col = joins_tables[join_name].c[column]
                cols += (col.label(f"c{i}_{col.name}"),)
                cols_mappings += ((joins_index[join_name], col.name),)
            except KeyError as error:
                raise InvalidColumnError(
                    column, joins_tables[join_name].element
                ) from error

    # Build SELECT ... FROM ... JOIN ... query
    query = get_select_join_query(state, cols)

    # Build tuples with primary key names and mappings
    keys: Tuple[str, ...] = (root.primary_key[0].name,)
    mappings: Tuple[DBMapping, ...] = (
        namedtuple(
            "Result",
            (c for c in columns if "." not in c and c != skip_columns[0]),
        ),
    )

    for i, join_on in enumerate(joins_names, 1):
        keys += (joins_tables[join_on].primary_key[0].name,)

        table_cols = []
        for table_index, col in cols_mappings:
            if table_index == i:
                table_cols.append(col)

        mappings += (
            namedtuple(
                "Result",
                (c for c in table_cols if c != skip_columns[i]),
            ),
        )

    # Fetch results and convert them to models
    types_count = 1 + len(joins_names)
    results = []

    for record in await database.fetch_all(query):
        tables_data: TablesData = tuple({} for _ in range(types_count))
        for col, value in enumerate(record_tuple(record)):
            col_table, col_name = cols_mappings[col]
            tables_data[col_table][col_name] = value

        mapped_record: Tuple[DBMapping, ...] = tuple()
        for i, data in enumerate(tables_data):
            if data[keys[i]] is None:
                mapped_record += (None,)
            else:
                if skip_columns[i]:
                    data.pop(skip_columns[i])
                mapped_record += (mappings[i](**data),)

        results.append(mapped_record)

    return results


async def select_with_joins_anonymous_columns(
    state: QueryState,
    columns: Sequence[str],
) -> List[DBMapping]:
    join_root = cast(TableClause, state.join_root)
    joins_tables = cast(Dict[str, TableClause], state.join_tables)

    cols: Tuple[ColumnElement, ...] = tuple()
    for i, column in enumerate(columns):
        if "." not in column:
            try:
                col = join_root.c[column]
                cols += (col,)
            except KeyError as error:
                raise InvalidColumnError(column, state.table) from error
        else:
            join_name, column = column.rsplit(".", 1)
            try:
                col = joins_tables[join_name].c[column]
                cols += (col.label(f"c{i}_{col.name}"),)
            except KeyError as error:
                raise InvalidColumnError(
                    column, joins_tables[join_name].element
                ) from error

    query = get_select_join_query(state, cols)
    return [record_tuple(record) for record in await database.fetch_all(query)]


def get_select_join_query(
    state: QueryState,
    columns: Sequence[ColumnElement],
    ordered: bool = True,
) -> ClauseElement:
    query = select(columns).select_from(get_join_select_from(state))
    query = filter_query(state, query, in_join=True)
    query = slice_query(state, query)
    if ordered:
        query = order_query(state, query, in_join=True)
    return query


def get_join_select_from(state: QueryState) -> ClauseElement:
    joins_tables = cast(Dict[str, TableClause], state.join_tables)
    query_from = cast(TableClause, state.join_root)

    for join_on, join_table in joins_tables.items():
        if "." in join_on:
            left_table_name, join_on = join_on.rsplit(".", 1)
            left_table = joins_tables[left_table_name]
        else:
            left_table = state.join_root

        join_left = left_table.c[join_on]
        foreign_key, *_ = join_left.foreign_keys
        join_column = join_table.c[foreign_key.column.name]
        query_from = query_from.outerjoin(join_table, join_left == join_column)

    return query_from


def record_tuple(record: Record) -> Tuple[Any, ...]:
    return tuple(record[r] for r in record)


def record_dict(record: Record) -> dict:
    return {r: record[r] for r in record}
