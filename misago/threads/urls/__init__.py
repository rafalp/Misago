# flake8: noqa
from misago.threads.urls import events, posts, privatethreads, threads


urlpatterns = []

urlpatterns += events.urlpatterns
urlpatterns += posts.urlpatterns
urlpatterns += privatethreads.urlpatterns
urlpatterns += threads.urlpatterns
