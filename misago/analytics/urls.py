from django.urls import path

from .views import google_site_verification

urlpatterns = [
    path(
        "google<slug:token>.html",
        google_site_verification,
        name="google-site-verification",
    )
]
