from django.conf.urls import patterns, url


urlpatterns = patterns('misago.legal.views',
    url(r'^terms-of-service/$', 'terms', name='terms_of_service'),
    url(r'^privacy-policy/$', 'privacy_policy', name='privacy_policy'),
)
