from django.conf import settings
from django.urls import NoReverseMatch, path, reverse

from .views import login


urlpatterns = [path("login/", login, name="login")]


def get_login_url():
    try:
        return reverse(settings.LOGIN_URL)
    except NoReverseMatch:
        return settings.LOGIN_URL
