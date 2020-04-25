from sqlalchemy import func
from sqlalchemy.sql import ClauseElement, TableClause, select


def count(table: TableClause) -> ClauseElement:
    return select([func.count()]).select_from(table)
