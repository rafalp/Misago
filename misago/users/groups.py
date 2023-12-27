from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()


def count_groups_members() -> list[tuple[int, int]]:
    with connection.cursor() as cursor:
        user_table = User._meta.db_table
        cursor.execute(
            f"SELECT UNNEST(groups_ids) AS gid, COUNT(*) FROM {user_table} GROUP BY gid;"
        )
        return list(map(tuple, cursor.fetchall()))
