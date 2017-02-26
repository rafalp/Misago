from django.db import connections


def fetch_assoc(query, *args):
    """return all rows from a cursor as a dict"""
    with connections['misago05'].cursor() as cursor:
        cursor.execute(query, *args)

        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        while row:
            yield dict(zip(columns, row))
            row = cursor.fetchone()
