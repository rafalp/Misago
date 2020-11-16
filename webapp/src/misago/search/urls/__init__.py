from django.conf.urls import url

from ..views import landing, search

urlpatterns = [
    url(r"^search/$", landing, name="search"),
    url(r"^search/(?P<search_provider>[-a-zA-Z0-9]+)/$", search, name="search"),
]
