from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from ....conf import settings
from ....core.pgutils import chunk_queryset
from ...permissions import can_delete_own_account

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Deletes accounts of users that have requested it. "
        "Leaves their content behind, but anonymises it."
    )

    def handle(self, *args, **options):
        users_deleted = 0

        queryset = User.objects.filter(is_deleting_account=True)

        for user in chunk_queryset(queryset):
            if can_delete_own_account(user, user):
                user.delete()
                users_deleted += 1

        self.stdout.write("Deleted users: %s" % users_deleted)
