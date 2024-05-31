from django.urls import path

from .views import settings, validate


urlpatterns = [
    path("", settings.index, name="account-settings"),
    path(
        "preferences/",
        settings.AccountPreferencesView.as_view(),
        name="account-preferences",
    ),
    path(
        "username/",
        settings.AccountUsernameView.as_view(),
        name="account-username",
    ),
    path(
        "delete/",
        settings.AccountDeleteView.as_view(),
        name="account-delete",
    ),
    path(
        "delete/completed/",
        settings.account_delete_completed,
        name="account-delete-completed",
    ),
    path(
        "validate/email/",
        validate.email,
        name="account-validate-email",
    ),
    path(
        "validate/username/",
        validate.username,
        name="account-validate-username",
    ),
    path(
        "validate/password/",
        validate.password,
        name="account-validate-password",
    ),
]
