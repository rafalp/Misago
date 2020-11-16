from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^login/(?P<backend>[^/]+)/$", views.auth, name="social-begin"),
    url(r"^complete/(?P<backend>[^/]+)/$", views.complete, name="social-complete"),
]
