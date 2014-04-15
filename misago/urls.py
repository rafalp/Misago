from django.conf.urls import patterns, include, url


urlpatterns = patterns('misago.core',
    # "misago:index" link symbolises "root" of Misago links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago and will be handled by misago.views.exceptionhandler if it
    # results in Http404 or PermissionDenied exception
    url(r'^$', 'views.forum_index', name='index'),
)

# Register Misago Apps
urlpatterns += patterns('',
    url(r'^', include('misago.users.urls')),
)
