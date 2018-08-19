from django.core.management.base import BaseCommand
from django.utils import timezone

from misago.core.pgutils import chunk_queryset
from misago.users.datadownloads import expire_user_data_download
from misago.users.models import DataDownload


class Command(BaseCommand):
    help = "Expires old user data downloads."

    def handle(self, *args, **options):
        downloads_expired = 0
        queryset = DataDownload.objects.select_related('user')
        queryset = queryset.filter(
            status=DataDownload.STATUS_READY,
            expires_on__lte=timezone.now(),
        )

        for data_download in chunk_queryset(queryset):
            expire_user_data_download(data_download)
            downloads_expired += 1

        self.stdout.write("Data downloads expired: {}".format(downloads_expired))
