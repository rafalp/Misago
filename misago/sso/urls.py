from django.conf.urls import url

from .api import sync_user
from .client import MisagoAuthenticateView, MisagoLoginView

urlpatterns = [
    url(r"^sync/$", sync_user, name="simple-sso-user-sync"),
    url(r"^client/$", MisagoLoginView.as_view(), name="simple-sso-login"),
    url(
        r"^client/authenticate/$",
        MisagoAuthenticateView.as_view(),
        name="simple-sso-authenticate",
    ),
]
