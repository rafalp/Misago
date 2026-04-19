from django.urls import path

from .views import dismiss_dev_warning

urlpatterns = [
    path("dismiss-dev-warning/", dismiss_dev_warning, name="dismiss-dev-warning"),
]
