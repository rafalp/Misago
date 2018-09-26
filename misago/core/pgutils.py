from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.db.models import Index


class PgPartialIndex(Index):
    suffix = 'part'
    max_name_length = 31

    def __init__(self, fields=(), name=None, where=None):
        if not where:
            raise ValueError('partial index requires WHERE clause')
        self.where = where

        super(PgPartialIndex, self).__init__(fields=fields, name=name)

    def set_name_with_model(self, model):
        table_name = model._meta.db_table

        column_names = sorted(self.where.keys())
        where_items = []
        for key in sorted(self.where.keys()):
            where_items.append('{}:{}'.format(key, repr(self.where[key])))

        # The length of the parts of the name is based on the default max
        # length of 30 characters.
        hash_data = [table_name] + self.fields + where_items + [self.suffix]
        self.name = '%s_%s_%s' % (
            table_name[:11],
            column_names[0][:7],
            '%s_%s' % (self._hash_generator(*hash_data), self.suffix),
        )

        assert len(self.name) <= self.max_name_length, (
            'Index too long for multiple database support. Is self.suffix '
            'longer than 3 characters?'
        )
        self.check_name()

    def __repr__(self):
        if self.where is not None:
            where_items = []
            for key in sorted(self.where.keys()):
                where_items.append('='.join([
                    key,
                    repr(self.where[key])
                ]))
            return '<%(name)s: fields=%(fields)s, where=%(where)s>' % {
                'name': self.__class__.__name__,
                'fields': "'{}'".format(', '.join(self.fields)),
                'where': "'{}'".format(', '.join(where_items)),
            }
        else:
            return super(PgPartialIndex, self).__repr__()

    def deconstruct(self):
        path, args, kwargs = super(PgPartialIndex, self).deconstruct()
        kwargs['where'] = self.where
        return path, args, kwargs

    def create_sql(self, model, schema_editor, using=''):
        parameters = super(PgPartialIndex, self).create_sql(
            model, schema_editor, using)
        parameters.parts['extra'] = self.get_sql_extra(model, schema_editor)
        return str(parameters)

    def get_sql_extra(self, model, schema_editor):
        quote_name = schema_editor.quote_name
        quote_value = schema_editor.quote_value

        clauses = []
        for field, condition in self.where.items():
            field_name = None
            compr = None
            if field.endswith('__lt'):
                field_name = field[:-4]
                compr = '<'
            elif field.endswith('__gt'):
                field_name = field[:-4]
                compr = '>'
            elif field.endswith('__lte'):
                field_name = field[:-5]
                compr = '<='
            elif field.endswith('__gte'):
                field_name = field[:-5]
                compr = '>='
            else:
                field_name = field
                compr = '='

            column = model._meta.get_field(field_name).column
            clauses.append('{} {} {}'.format(
                quote_name(column), compr, quote_value(condition)))
        # sort clauses for their order to be determined and testable
        return ' WHERE {}'.format(' AND '.join(sorted(clauses)))


def chunk_queryset(queryset, chunk_size=20):
    ordered_queryset = queryset.order_by('-pk') # bias to newest items first
    chunk = ordered_queryset[:chunk_size]
    while chunk:
        last_pk = None
        for item in chunk:
            last_pk = item.pk
            yield item
        chunk = ordered_queryset.filter(pk__lt=last_pk)[:chunk_size]
