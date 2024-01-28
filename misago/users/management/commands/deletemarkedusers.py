from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....conf.shortcuts import get_dynamic_settings
from ...deletesrecord import record_user_deleted_by_self
from ...permissions import can_delete_own_account

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Deletes accounts of users that have requested it. "
        "Leaves their content behind, but anonymises it."
    )

    def handle(self, *args, **options):
        users_deleted = 0
        settings = get_dynamic_settings()

        queryset = User.objects.filter(is_deleting_account=True)

        for user in queryset.iterator(chunk_size=50):
            if can_delete_own_account(settings, user, user):
                user.delete(anonymous_username=settings.anonymous_username)
                record_user_deleted_by_self()
                users_deleted += 1

        self.stdout.write("Deleted users: %s" % users_deleted)
