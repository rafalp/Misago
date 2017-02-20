from django.core.paginator import Paginator
from django.db.migrations.operations import RunSQL


class CreatePartialIndex(RunSQL):
    CREATE_SQL = """
CREATE INDEX %(index_name)s ON %(table)s (%(field)s)
WHERE %(condition)s;
"""

    REMOVE_SQL = """
DROP INDEX %(index_name)s
"""

    def __init__(self, field, index_name, condition):
        self.model, self.field = field.split('.')
        self.index_name = index_name
        self.condition = condition

    @property
    def reversible(self):
        return True

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model)

        statement = self.CREATE_SQL % {
            'index_name': self.index_name,
            'table': model._meta.db_table,
            'field': self.field,
            'condition': self.condition,
        }

        schema_editor.execute(statement)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute(self.REMOVE_SQL % {'index_name': self.index_name})

    def describe(self):
        message = "Create PostgreSQL partial index on field %s in %s for %s"
        formats = (self.field, self.model_name, self.values)
        return message % formats


def batch_update(queryset, step=50):
    """
    Util because psycopg2 iterators aren't really memory effective
    """
    paginator = Paginator(queryset.order_by('pk'), step)
    for page_number in paginator.page_range:
        for obj in paginator.page(page_number).object_list:
            yield obj


def batch_delete(queryset, step=50):
    """
    Another util cos paginator goes bobbins when you are deleting
    """
    queryset_exists = True
    while queryset_exists:
        for obj in queryset[:step]:
            yield obj
        queryset_exists = queryset.exists()


class CreatePartialCompositeIndex(CreatePartialIndex):
    CREATE_SQL = """
CREATE INDEX %(index_name)s ON %(table)s (%(fields)s)
WHERE %(condition)s;
"""

    REMOVE_SQL = """
DROP INDEX %(index_name)s
"""

    def __init__(self, model, fields, index_name, condition):
        self.model = model
        self.fields = fields
        self.index_name = index_name
        self.condition = condition

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = from_state.apps.get_model(app_label, self.model)

        statement = self.CREATE_SQL % {
            'index_name': self.index_name,
            'table': model._meta.db_table,
            'fields': ', '.join(self.fields),
            'condition': self.condition,
        }

        schema_editor.execute(statement)

    def describe(self):
        message = ("Create PostgreSQL partial composite " "index on fields %s in %s for %s")
        formats = (', '.join(self.fields), self.model_name, self.values)
        return message % formats
