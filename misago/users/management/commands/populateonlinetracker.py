from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.core.pgutils import chunk_queryset
from misago.users.models import Online


UserModel = get_user_model()


class Command(BaseCommand):
    help = "Populates online tracker for user accounts that lack it."

    def handle(self, *args, **options):
        entries_created = 0
        queryset = UserModel.objects.filter(online_tracker__isnull=True)
        for user in chunk_queryset(queryset):
            Online.objects.create(user=user, last_click=user.last_login)
            entries_created += 1

        self.stdout.write("Tracker entries created: {}".format(entries_created))
