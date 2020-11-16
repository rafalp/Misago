from django.conf.urls import url

from .. import api

urlpatterns = [
    url(r"^search/$", api.search, name="search"),
    url(r"^search/(?P<search_provider>[-a-zA-Z0-9]+)/$", api.search, name="search"),
]
