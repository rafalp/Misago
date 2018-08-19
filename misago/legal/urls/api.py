from django.conf.urls import url

from misago.legal.api import submit_agreement


urlpatterns = [
    url(r'^submit-agreement/(?P<pk>\d+)/$', submit_agreement, name='submit-agreement'),
]
