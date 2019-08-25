from django.conf.urls import url

from .api import sso_sync
from .client import MisagoAuthenticateView, MisagoLoginView

urlpatterns = [
    url(r"^sync/$", sso_sync, name="simple-sso-sync"),
    url(r"^client/$", MisagoLoginView.as_view(), name="simple-sso-login"),
    url(
        r"^client/authenticate/$",
        MisagoAuthenticateView.as_view(),
        name="simple-sso-authenticate",
    ),
]
