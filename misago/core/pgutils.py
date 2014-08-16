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

    def database_forwards(self, app_label, schema_editor,
                          from_state, to_state):
        apps = from_state.render()
        model = apps.get_model(app_label, self.model)

        statement = self.CREATE_SQL % {
            'index_name': self.index_name,
            'table': model._meta.db_table,
            'field': self.field,
            'condition': self.condition,
        }

        schema_editor.execute(statement)

    def database_backwards(self, app_label, schema_editor,
                           from_state, to_state):
        schema_editor.execute(
            self.REMOVE_SQL % {'index_name': self.index_name})

    def describe(self):
        message = "Create PostgreSQL partial index on field %s in %s for %s"
        formats = (self.field, self.model_name, self.values)
        return message % formats
