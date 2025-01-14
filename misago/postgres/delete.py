from typing import Type

from django.db.models import Model

from .execute import execute_rowcount


def delete_one(obj: Model) -> int:
    """Deletes an object from the database, bypassing all Django ORM logic.

    Returns a number of deleted rows.
    """
    table = obj._meta.db_table
    pkey = obj._meta.pk.column

    return execute_rowcount(f'DELETE FROM "{table}" WHERE "{pkey}" = %s;', [obj.pk])


def delete_all(model: Type[Model], **where):
    """Deletes multiple rows from the database, bypassing all Django ORM logic.

    Requires at least ONE kwarg with a name of model field to use in the delete:

    `delete_all(User, group_id=9)` executes the
    `DELETE FROM "misago_users_user" WHERE "group_id" = 9;` query.
    `delete_all(User, pk=[1, 3, 4])` executes the
    `DELETE FROM "misago_users_user" WHERE "id" IN (1, 3, 4);` query.

    Multiple kwargs are joined with the "AND" keyword:

    `delete_all(User, group_id=9, is_misago_admin=False)` will execute the
    `DELETE FROM "misago_users_user" WHERE "group_id" = 9 AND "is_misago_admin" = FALSE;`
    query.

    Returns a number of deleted rows.
    """
    if not where:
        raise ValueError("At least one 'WHERE' clause is required.")

    fields = []
    params = []
    for field, value in where.items():
        column = model._meta.get_field(field).column
        if isinstance(value, list):
            in_clause = ", ".join(["%s"] * len(value))
            fields.append(f'"{column}" IN ({in_clause})')
            params += [(v.pk if isinstance(v, Model) else v) for v in value]
        else:
            fields.append(f'"{column}" = %s')
            params.append(value.pk if isinstance(value, Model) else value)

    table = model._meta.db_table
    where_joined = " AND ".join(fields)

    return execute_rowcount(f'DELETE FROM "{table}" WHERE {where_joined};', params)
