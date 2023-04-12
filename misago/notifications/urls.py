from django.urls import path

from .views import notification, notifications

urlpatterns = [
    path("notification/<int:notification_id>/", notification, name="notification"),
    path("notifications/", notifications, name="notifications"),
    path("notifications/unread/", notifications, name="notifications-unread"),
    path("notifications/read/", notifications, name="notifications-read"),
]
