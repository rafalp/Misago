from django.urls import path

from .. import api

urlpatterns = [
    path("search/", api.search, name="search"),
    path("search/<slug:search_provider>/", api.search, name="search"),
]
