from .models import DataDownload


STATUS_PROGRESS = (DataDownload.STATUS_PENDING, DataDownload.STATUS_PROCESSING)


def is_user_preparing_data_download(user):
    queryset = DataDownload.objects.filter(user=user, status__in=STATUS_PROGRESS)
    return queryset.exists()


def prepare_user_data_download(user, requester=None):
    requester = requester or user

    return DataDownload.objects.create(
        user=user,
        requester=requester,
        requester_name=requester.username,
    )


def expire_user_data_download(download):
    download.status = DataDownload.STATUS_EXPIRED
    if download.file:
        download.file.delete(save=False)
    download.save()
    