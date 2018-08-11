from __future__ import unicode_literals

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.conf import settings
from misago.core.pgutils import chunk_queryset


UserModel = get_user_model()


class Command(BaseCommand):
    help = (
        "Deletes inactive user accounts older than set time."
    )

    def handle(self, *args, **options):
        if not settings.MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS:
            self.stdout.write("Automatic deletion of inactive users is currently disabled.")
            return


        users_deleted = 0
        
        joined_on_cutoff = timezone.now() - timedelta(
            days=settings.MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS)

        queryset = UserModel.objects.filter(
            requires_activation__gt=UserModel.ACTIVATION_NONE,
            joined_on__lt=joined_on_cutoff,
        )

        for user in chunk_queryset(queryset):
            user.delete()
            users_deleted += 1

        self.stdout.write("Deleted users: {}".format(users_deleted))
