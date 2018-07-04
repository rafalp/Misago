from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from misago.conf import settings
from misago.core.pgutils import chunk_queryset
from misago.users.models import DataDownload

UserModel = get_user_model()


class Command(BaseCommand):
    help = "Processes user data downloads."

    def handle(self, *args, **options):
        if not settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR:
            self.stdout.write(
                "Data downloads working directory has to be set for this feature to work.")
            return
        
