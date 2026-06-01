from django.urls import path

from .views import oauth2_complete, oauth2_login

urlpatterns = [
    path("oauth2/login/", oauth2_login, name="oauth2-login"),
    path("oauth2/complete/", oauth2_complete, name="oauth2-complete"),
]
