from django.contrib.auth import get_user_model

from ..postgres.execute import execute_fetch_all

User = get_user_model()


def count_groups_members() -> list[tuple[int, int]]:
    """Returns a list of (group id, members count) tuples.

    Excludes groups without any members from results.
    """

    user_table = User._meta.db_table
    result = execute_fetch_all(
        f'SELECT UNNEST("groups_ids") AS "gid", COUNT(*) FROM "{user_table}" GROUP BY "gid";'
    )
    return list(map(tuple, result))
