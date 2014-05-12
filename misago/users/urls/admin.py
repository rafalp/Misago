from django.conf.urls import patterns, url, include
from misago.users.views.useradmin import UsersList


action_urlpatterns = patterns('',
    url(r'^$', UsersList.as_view(), name='index'),
)


section_urlpatterns = patterns('',
    url(r'^accounts/', include(action_urlpatterns, namespace='accounts')),
)


urlpatterns = patterns('',
    url(r'^users/', include(section_urlpatterns, namespace='users')),
)
