from django.urls import path

from .views import settings


urlpatterns = [
    path("", settings.index, name="account-settings"),
    path(
        "preferences/",
        settings.AccountPreferencesView.as_view(),
        name="account-preferences",
    ),
]
