from django.urls import path

from .api import sso_sync
from .client import MisagoAuthenticateView, MisagoLoginView

urlpatterns = [
    path("sync/", sso_sync, name="simple-sso-sync"),
    path("client/", MisagoLoginView.as_view(), name="simple-sso-login"),
    path(
        "client/authenticate/",
        MisagoAuthenticateView.as_view(),
        name="simple-sso-authenticate",
    ),
]
