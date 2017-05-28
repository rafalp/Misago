from django.conf.urls import include, url
from django.views.generic import TemplateView

from misago.conf import settings
from misago.core.views import forum_index


app_name = 'misago'

# Register Misago Apps
urlpatterns = [
    url(r'^', include('misago.legal.urls')),
    url(r'^', include('misago.users.urls')),
    url(r'^', include('misago.categories.urls')),
    url(r'^', include('misago.threads.urls')),
    url(r'^', include('misago.search.urls')),

    # default robots.txt
    url(
        r'^robots.txt$',
        TemplateView.as_view(content_type='text/plain', template_name='misago/robots.txt')
    ),

    # "misago:index" link symbolises "root" of Misago links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago and will be handled by misago.views.exceptionhandler if it
    # results in Http404 or PermissionDenied exception
    url(r'^$', forum_index, name='index'),
]


# Register API
apipatterns = [
    url(r'^', include('misago.categories.urls.api')),
    url(r'^', include('misago.markup.urls')),
    url(r'^', include('misago.threads.urls.api')),
    url(r'^', include('misago.users.urls.api')),
    url(r'^', include('misago.search.urls.api')),
]

urlpatterns += [
    url(r'^api/', include((apipatterns, 'api'), namespace='api')),
]


# Register Misago ACP
if settings.MISAGO_ADMIN_PATH:
    # Admin patterns recognised by Misago
    adminpatterns = [
        url(r'^', include('misago.admin.urls')),
    ]

    admin_prefix = r'^%s/' % settings.MISAGO_ADMIN_PATH
    urlpatterns += [
        url(admin_prefix, include((adminpatterns, 'admin'), namespace='admin')),
    ]
