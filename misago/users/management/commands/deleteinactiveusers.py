from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from ....conf import settings
from ....core.pgutils import chunk_queryset

User = get_user_model()


class Command(BaseCommand):
    help = "Deletes inactive user accounts older than set time."

    def handle(self, *args, **options):
        if not settings.MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS:
            self.stdout.write(
                "Automatic deletion of inactive users is currently disabled."
            )
            return

        users_deleted = 0

        joined_on_cutoff = timezone.now() - timedelta(
            days=settings.MISAGO_DELETE_NEW_INACTIVE_USERS_OLDER_THAN_DAYS
        )

        queryset = User.objects.filter(
            requires_activation__gt=User.ACTIVATION_NONE, joined_on__lt=joined_on_cutoff
        )

        for user in chunk_queryset(queryset):
            user.delete()
            users_deleted += 1

        self.stdout.write("Deleted users: %s" % users_deleted)
