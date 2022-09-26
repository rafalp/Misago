from django.urls import path

from .views import healthcheck

urlpatterns = [path("healthcheck/", healthcheck, name="healthcheck")]
