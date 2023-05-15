from django.urls import path

from .views import disable_email_notifications, notification, notifications

urlpatterns = [
    path(
        "notifications/disable-email/<int:watched_thread_id>/<str:secret>/",
        disable_email_notifications,
        name="notifications-disable-email",
    ),
    path("notification/<int:notification_id>/", notification, name="notification"),
    path("notifications/", notifications, name="notifications"),
    path("notifications/unread/", notifications, name="notifications-unread"),
    path("notifications/read/", notifications, name="notifications-read"),
]
