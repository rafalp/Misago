from django.urls import path

from .views import debug_search

urlpatterns = [
    path("search/", debug_search, name="search"),
]
