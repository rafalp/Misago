from django.urls import path

from .views import oauth_login, oauth_complete

urlpatterns = [
    path("oauth/login/", oauth_login, name="oauth-login"),
    path("oauth/complete/", oauth_complete, name="oauth-complete"),
]
