from django.conf.urls import patterns, url


urlpatterns = patterns('misago.legal.views',
    url(r'^(?P<page>[\w\d-]+)/$', 'legal_page'),
)

