from django.conf.urls import url

from .views import healthcheck

urlpatterns = [url(r"^healthcheck/$", healthcheck, name="healthcheck")]
