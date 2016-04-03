from django.conf.urls import patterns, url


urlpatterns = patterns('misago.legal.views',
    url(r'^terms-of-service/$', 'terms_of_service', name='terms-of-service'),
    url(r'^privacy-policy/$', 'privacy_policy', name='privacy-policy'),
)
