import logging

from django.core.management.base import BaseCommand

from misago.conf import settings
from misago.core.pgutils import chunk_queryset
from misago.users.datadownloads import prepare_user_data_download
from misago.users.models import DataDownload


logger = logging.getLogger('misago.users.datadownloads')


class Command(BaseCommand):
    help = "Prepares user data downloads."

    def handle(self, *args, **options):
        working_dir = settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR
        if not working_dir:
            self.stdout.write(
                "MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR has to be set in order for "
                "this feature to work.")
            return
        
        downloads_prepared = 0
        queryset = DataDownload.objects.select_related('user')
        queryset = queryset.filter(status=DataDownload.STATUS_PENDING)
        for data_download in chunk_queryset(queryset):
            if prepare_user_data_download(data_download, logger):
                downloads_prepared += 1

        self.stdout.write("Data downloads prepared: {}".format(downloads_prepared))
