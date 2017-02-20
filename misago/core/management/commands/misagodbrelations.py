from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField


class Command(BaseCommand):
    help = 'Lists relations between models'

    def handle(self, *args, **options):
        relation_fields = (ForeignKey, OneToOneField, ManyToManyField)
        field_pattern = "%s=%s(%s, on_delete=%s)\n"

        for app in apps.get_app_configs():
            app_header_printed = False
            if app.name.startswith('misago.') and app.models_module:
                for model in app.get_models():
                    # Search model for relations
                    model_relations = []
                    for field in model._meta.fields:
                        if isinstance(field, relation_fields):
                            model_relations.append(field)

                    # If model has relations, print them
                    if model_relations:
                        if not app_header_printed:
                            # Lazy print app header
                            self.print_app_header(app)
                            app_header_printed = True

                        # Print model header
                        self.print_model_header(model)

                        # Finally list model relations
                        for field in model_relations:
                            self.stdout.write(
                                field_pattern % (
                                    field.name, field.__class__.__name__,
                                    field.related_model.__name__, field.rel.on_delete.__name__,
                                )
                            )

    def print_app_header(self, app):
        # Fancy title
        self.stdout.write("\n\n%s" % app.name)
        self.stdout.write('=' * len(app.name))

    def print_model_header(self, model):
        self.stdout.write("\n%s" % model.__name__)
        self.stdout.write('-' * len(model.__name__))
        self.stdout.write("\n")
