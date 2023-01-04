from django.urls import path

from .views import oauth_start, oauth_redirect

urlpatterns = [
    path("oauth/start/", oauth_start, name="oauth-start"),
    path("oauth/redirect/", oauth_redirect, name="oauth-redirect"),
]
