from django.urls import include, path

app_name = "apiv2"

urlpatterns = [
    path("", include("misago.apiv2.notifications.urls")),
    path("", include("misago.apiv2.threads.urls")),
]
