from datetime import timedelta

from django.utils import timezone

from ...conf import settings
from ..models import DataDownload
from ..signals import archive_user_data

from .dataarchive import DataArchive


STATUS_REQUEST = (DataDownload.STATUS_PENDING, DataDownload.STATUS_PROCESSING)


def user_has_data_download_request(user):
    queryset = DataDownload.objects.filter(user=user, status__in=STATUS_REQUEST)
    return queryset.exists()


def request_user_data_download(user, requester=None):
    requester = requester or user

    return DataDownload.objects.create(
        user=user, requester=requester, requester_name=requester.username
    )


def prepare_user_data_download(download, expires_in, logger=None):
    working_dir = settings.MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR
    user = download.user
    with DataArchive(user, working_dir) as archive:
        try:
            archive_user_data.send(user, archive=archive)
            download.status = DataDownload.STATUS_READY
            download.expires_on = timezone.now() + timedelta(hours=expires_in)
            download.file = archive.get_file()
            download.save()
            # todo: send an e-mail with download link
            return True
        except Exception as e:  # pylint: disable=broad-except
            if logger:
                logger.exception(e, exc_info=e)
            return False


def expire_user_data_download(download):
    download.status = DataDownload.STATUS_EXPIRED
    if download.file:
        download.file.delete(save=False)
    download.save()
