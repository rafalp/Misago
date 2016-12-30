from django.db import connections


def fetch_assoc(query, *args):
    """
    Return all rows from a cursor as a dict
    """
    cursor = connections['misago05'].cursor()
    cursor.execute(query, *args)

    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    while row:
        yield dict(zip(columns, row))
        row = cursor.fetchone()
