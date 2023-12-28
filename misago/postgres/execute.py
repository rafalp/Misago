from typing import Any

from django.db import connection


def execute_fetch_all(query: str, params: dict | list | None = None) -> list[tuple]:
    """Executes a raw query and returns all rows."""
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_fetch_one(query: str, params: dict | list | None = None) -> tuple:
    """Executes a raw query and returns one row."""
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()


def execute_rowcount(query: str, params: dict | list | None = None) -> int:
    """Executes a raw query and returns a number of affected rows."""
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.rowcount
