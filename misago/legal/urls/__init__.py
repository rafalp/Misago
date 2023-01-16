from django.urls import path

from ..views import privacy_policy, terms_of_service

urlpatterns = [
    path("privacy-policy/", privacy_policy, name="privacy-policy"),
    path("terms-of-service/", terms_of_service, name="terms-of-service"),
]
