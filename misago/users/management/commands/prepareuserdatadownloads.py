import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from misago.conf import settings
from misago.core.pgutils import chunk_queryset
from misago.users.datacollector import DataCollector
from misago.users.models import DataDownload


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
            data_collector = DataCollector(data_download.user, working_dir)
            try:
                collect_user_data(data_download.user, data_collector)
                data_collector.create_archive()
                data_download.save()
            except Exception as e:
                print(e)
                logger.exception(e)
            data_collector.delete_tmp_dir()

            downloads_prepared += 1

        self.stdout.write("Data downloads prepared: {}".format(downloads_prepared))


def collect_user_data(user, data_collector):
    data_collector.write_json_file('details', {
        'username': user.username,
        'email': user.email,
    })

    avatars = data_collector.create_collection('avatars')
    avatars.write_file(user.avatar_tmp)
    avatars.write_file(user.avatar_src)
    for avatar in user.avatar_set.iterator():
        avatars.write_file(avatar.image)
