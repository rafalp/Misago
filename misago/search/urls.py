from django.urls import path

from .views import debug_search

urlpatterns = [path("debug-search/", debug_search)]
