from django.conf.urls import url
from .client import MisagoAuthenticateView, MisagoLoginView

urlpatterns = [
    url(r"^client/$", MisagoLoginView.as_view(), name="simple-sso-login"),
    url(
        r"^client/authenticate/$",
        MisagoAuthenticateView.as_view(),
        name="simple-sso-authenticate",
    ),
]
