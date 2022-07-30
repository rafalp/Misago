from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from sqlalchemy.sql import ClauseElement, TableClause


@dataclass
class QueryState:
    """Holds state that's used to build database query."""

    table: TableClause
    filter: Optional[List[ClauseElement | dict]] = None
    exclude: Optional[List[ClauseElement | dict]] = None
    distinct: bool = False
    join: Optional[List[str]] = None
    join_root: Optional[TableClause] = None
    join_tables: Optional[Dict[str, TableClause]] = None
    order_by: Optional[Sequence[str]] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    subquery: Optional[str] = None
