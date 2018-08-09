import logging

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext

from misago.conf import settings
from misago.core.mail import mail_user
from misago.core.pgutils import chunk_queryset
from misago.users.datadownloads import prepare_user_data_download
from misago.users.models import DataDownload


logger = logging.getLogger('misago.users.datadownloads')


class Command(BaseCommand):
    help = "Prepares user data downloads."
    leave_locale_alone = True

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
                user = data_download.user
                subject = ugettext("%(user)s, your data download is ready") % { 'user': user }
                mail_user(user, subject, 'misago/emails/data_download', context={
                    'data_download': data_download,
                    'expires_in': settings.MISAGO_USER_DATA_DOWNLOADS_EXPIRE_IN_HOURS,
                })

                downloads_prepared += 1

        self.stdout.write("Data downloads prepared: {}".format(downloads_prepared))
