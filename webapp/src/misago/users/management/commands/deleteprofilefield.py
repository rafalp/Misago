from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....core.pgutils import chunk_queryset

User = get_user_model()


class Command(BaseCommand):
    help = "Deletes specified profile field from database."

    def add_arguments(self, parser):
        parser.add_argument("fieldname", help="field to delete", nargs="?")

    def handle(self, *args, **options):
        fieldname = options["fieldname"]
        if not fieldname:
            self.stderr.write("Specify fieldname to delete.")
            return

        fields_deleted = 0

        queryset = User.objects.filter(profile_fields__has_keys=[fieldname])

        for user in chunk_queryset(queryset):
            if fieldname in user.profile_fields.keys():
                user.profile_fields.pop(fieldname)
                user.save(update_fields=["profile_fields"])
                fields_deleted += 1

        self.stdout.write(
            '"%s" profile field has been deleted from %s users.'
            % (fieldname, fields_deleted)
        )
