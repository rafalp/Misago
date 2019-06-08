from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from ....conf.shortcuts import get_dynamic_settings
from ....core.pgutils import chunk_queryset

User = get_user_model()


class Command(BaseCommand):
    help = "Deletes inactive user accounts older than set time."

    def handle(self, *args, **options):
        settings = get_dynamic_settings()
        if not settings.new_inactive_accounts_delete:
            self.stdout.write(
                "Automatic deletion of inactive user accounts is currently disabled."
            )
            return

        users_deleted = 0

        joined_on_cutoff = timezone.now() - timedelta(
            days=settings.new_inactive_accounts_delete
        )

        queryset = User.objects.filter(
            requires_activation__gt=User.ACTIVATION_NONE, joined_on__lt=joined_on_cutoff
        )

        for user in chunk_queryset(queryset):
            user.delete(anonymous_username=settings.anonymous_username)
            users_deleted += 1

        self.stdout.write("Deleted inactive user accounts: %s" % users_deleted)
