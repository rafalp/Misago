from .models import DataExport


STATUS_PROGRESS = (DataExport.STATUS_PENDING, DataExport.STATUS_PROCESSING)


def is_user_data_export_in_progress(user):
    queryset = DataExport.objects.filter(user=user, status__in=STATUS_PROGRESS)
    return queryset.exists()


def start_data_export_for_user(user, requester=None):
    requester = requester or user

    return DataExport.objects.create(
        user=user,
        requester=requester,
        requester_name=requester.username,
    )
