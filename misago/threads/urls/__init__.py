# flake8: noqa
from misago.threads.urls import privatethreads, threads


urlpatterns = threads.urlpatterns
urlpatterns += privatethreads.urlpatterns
