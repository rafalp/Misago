from django.conf.urls import url

from .views import privacy_policy, terms_of_service


urlpatterns = [
    url(r'^privacy-policy/$', privacy_policy, name='privacy-policy'),
    url(r'^terms-of-service/$', terms_of_service, name='terms-of-service'),
]
