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
        "details/",
        settings.AccountDetailsView.as_view(),
        name="account-details",
    ),
    path(
        "username/",
        settings.AccountUsernameView.as_view(),
        name="account-username",
    ),
    path(
        "password/",
        settings.AccountPasswordView.as_view(),
        name="account-password",
    ),
    path(
        "email/",
        settings.AccountEmailView.as_view(),
        name="account-email",
    ),
    path(
        "email/confirm/",
        settings.AccountEmailConfirmView.as_view(),
        name="account-email-confirm-sent",
    ),
    path(
        "email/confirm/<int:user_id>/<token>/",
        settings.account_email_confirm_change,
        name="account-email-confirm-change",
    ),
    path(
        "attachments/",
        settings.AccountAttachmentsView.as_view(),
        name="account-attachments",
    ),
    path(
        "download-data/",
        settings.AccountDownloadDataView.as_view(),
        name="account-download-data",
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
