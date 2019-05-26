from django.conf.urls import url

from .views import google_site_verification

urlpatterns = [
    url(
        r"^google(?P<token>[a-z0-9]+)\.html$",
        google_site_verification,
        name="google-site-verification",
    )
]
