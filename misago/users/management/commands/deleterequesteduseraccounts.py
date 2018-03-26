from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError, BaseCommand

from misago.core.pgutils import chunk_queryset


UserModel = get_user_model()


class Command(BaseCommand):
    help = "Deletes accounts of users that have choosen to delete their account."

    def handle(self, *args, **options):
        deleted = 0

        queryset = UserModel.objects.filter(delete_own_account=True)

        for user in chunk_queryset(queryset):
            user.delete()
            deleted += 1

        self.stdout.write('{} user accounts have been deleted.'.format(deleted))
