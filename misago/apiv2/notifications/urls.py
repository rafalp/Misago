from django.urls import path

from .views import notifications, notifications_read_all

urlpatterns = [
    path(
        "notifications/",
        notifications,
        name="notifications",
    ),
    path(
        "notifications/read-all/",
        notifications_read_all,
        name="notifications-read-all",
    ),
]
