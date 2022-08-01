from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, TypeAlias

from sqlalchemy.sql import ClauseElement, TableClause

Lookup: TypeAlias = ClauseElement | Dict[str, Any]
LookupsList: TypeAlias = List[Lookup]


@dataclass
class QueryState:
    """Holds state that's used to build database query."""

    table: TableClause
    filter: Optional[List[Lookup]] = None
    exclude: Optional[List[Lookup]] = None
    or_filter: Optional[List[LookupsList]] = None
    or_exclude: Optional[List[LookupsList]] = None
    distinct: bool = False
    join: Optional[List[str]] = None
    join_root: Optional[TableClause] = None
    join_tables: Optional[Dict[str, TableClause]] = None
    order_by: Optional[Sequence[str]] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    subquery: Optional[str] = None
