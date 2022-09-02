from django.urls import path

from ..views import landing, search

urlpatterns = [
    path("search/", landing, name="search"),
    path("search/<slug:search_provider>/", search, name="search"),
]
