from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('misago.core.views',
    # "misago:index" link symbolises "root" of Misago links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago and will be handled by misago.views.exceptionhandler if it
    # results in Http404 or PermissionDenied exception
    url(r'^$', 'forum_index', name='index'),
)

# Register Misago Apps
urlpatterns += patterns('',
    url(r'^', include('misago.users.urls')),
)


# Register Misago ACP
if settings.MISAGO_ADMIN_PATH:
    # Admin patterns recognised by Misago
    adminpatterns = patterns('',
        url(r'^', include('misago.admin.urls')),
    )

    admin_prefix = r'^%s/' % settings.MISAGO_ADMIN_PATH
    urlpatterns += patterns('',
        url(admin_prefix, include(adminpatterns, namespace='admin')),
    )
