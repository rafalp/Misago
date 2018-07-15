import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.conf import settings
from misago.core.pgutils import chunk_queryset
from misago.users.dataarchive import DataArchive
from misago.users.models import DataDownload
from misago.users.signals import archive_user_personal_data


logger = logging.getLogger('misago.users.datadownloads')

UserModel = get_user_model()


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
            user = data_download.user
            with DataArchive(user, working_dir) as archive:
                try:
                    archive_user_personal_data.send(user, archive=archive)
                    data_download.file = archive.get_file()
                    #data_download.save()
                except Exception as e:
                    print(e)
                    logger.exception(e)

            downloads_prepared += 1

        self.stdout.write("Data downloads prepared: {}".format(downloads_prepared))
