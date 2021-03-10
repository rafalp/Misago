from django.conf.urls import url

from bh_settings import get_settings

from . import views


urlpatterns = []

if get_settings("enable_misago_social_urls"):
    urlpatterns.extend([
        url(r"^login/(?P<backend>[^/]+)/$", views.auth, name="social-begin"),
        url(r"^complete/(?P<backend>[^/]+)/$", views.complete, name="social-complete"),
    ])
