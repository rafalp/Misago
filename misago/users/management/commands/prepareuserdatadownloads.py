import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.conf import settings
from misago.core.pgutils import chunk_queryset
from misago.users.dataarchiver import DataArchiver
from misago.users.models import DataDownload
from misago.users.signals import archive_user_data


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
            data_archiver = DataArchiver(user, working_dir)
            try:
                archive_user_data.send(user, data_archiver=data_archiver)
                data_archiver.create_archive()
                #data_download.save()
            except Exception as e:
                print(e)
                logger.exception(e)
            # data_archiver.delete_archive()
            data_archiver.delete_tmp_dir()

            downloads_prepared += 1

        self.stdout.write("Data downloads prepared: {}".format(downloads_prepared))
