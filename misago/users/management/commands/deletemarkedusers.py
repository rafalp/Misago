from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....conf.shortcuts import get_dynamic_settings
from ...delete import DeleteUserContentAction, delete_user
from ...deletesrecord import record_user_deleted_by_self
from ...permissions import can_delete_own_account

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Deletes accounts of users that have requested it. "
        "Leaves their content behind, but anonymises it."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "content",
            nargs="?",
            type=str,
            default=DeleteUserContentAction.LEAVE.value,
            choices=[e.value for e in list(DeleteUserContentAction)],
            help="What to do with deleted user content",
        )

    def handle(self, *args, **options):
        users_deleted = 0
        settings = get_dynamic_settings()

        queryset = User.objects.filter(is_deleting_account=True)

        for user in queryset.iterator(chunk_size=50):
            if can_delete_own_account(settings, user, user):
                delete_user(
                    user,
                    content_action=DeleteUserContentAction[options["content"]],
                    anonymous_username=settings.anonymous_username,
                )
                record_user_deleted_by_self()
                users_deleted += 1

        self.stdout.write("Deleted users: %s" % users_deleted)
