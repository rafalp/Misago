from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError, BaseCommand


UserModel = get_user_model()


class Command(BaseCommand):
    help = (
        "Deletes specified profile field from database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'fieldname',
            help="field to delete",
            nargs='?',
        )

    def handle(self, *args, **options):
        fieldname = options['fieldname']
        if not fieldname:
            self.stderr.write("Specify fieldname to delete.")
            return

        deleted = 0

        queryset = UserModel.objects.filter(
            profile_fields__has_keys=[fieldname],
        )

        for user in queryset.iterator():
            if fieldname in user.profile_fields.keys():
                user.profile_fields.pop(fieldname)
                user.save(update_fields=['profile_fields'])
                deleted += 1

        self.stdout.write(
            '"{}" profile field has been deleted from {} users.'.format(
                fieldname, deleted
            )
        )
