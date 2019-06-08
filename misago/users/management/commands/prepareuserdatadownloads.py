import logging

from django.core.management.base import BaseCommand
from django.utils.translation import gettext

from ....conf import settings
from ....conf.shortcuts import get_dynamic_settings
from ....core.mail import mail_user
from ....core.pgutils import chunk_queryset
from ...datadownloads import prepare_user_data_download
from ...models import DataDownload

logger = logging.getLogger("misago.users.datadownloads")


class Command(BaseCommand):
    help = "Prepares user data downloads."
    leave_locale_alone = True

    def handle(self, *args, **options):
        working_dir = settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR
        if not working_dir:
            self.stdout.write(
                "MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR has to be set in order for "
                "this feature to work."
            )
            return

        dynamic_settings = get_dynamic_settings()
        expires_in = dynamic_settings.data_downloads_expiration

        downloads_prepared = 0
        queryset = DataDownload.objects.select_related("user")
        queryset = queryset.filter(status=DataDownload.STATUS_PENDING)
        for data_download in chunk_queryset(queryset):
            if prepare_user_data_download(data_download, expires_in, logger):
                user = data_download.user
                subject = gettext("%(user)s, your data download is ready") % {
                    "user": user
                }
                mail_user(
                    user,
                    subject,
                    "misago/emails/data_download",
                    context={
                        "data_download": data_download,
                        "expires_in": expires_in,
                        "settings": dynamic_settings,
                    },
                )

                downloads_prepared += 1

        self.stdout.write("Data downloads prepared: %s" % downloads_prepared)
