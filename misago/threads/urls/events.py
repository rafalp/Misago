from django.conf.urls import patterns, include, url
from misago.threads.views.events import EventsView


urlpatterns = patterns('',
    url(r'^edit-event/(?P<event_id>\d+)/$', EventsView.as_view(), name='edit_event'),
)
