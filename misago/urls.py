from django.urls import include, path
from django.views.generic import TemplateView

from . import hooks
from .conf import settings
from .forumindex.views import forum_index
from .parser.views import formatting_help

app_name = "misago"

# Register Misago Apps
urlpatterns = [
    path("", include("misago.analytics.urls")),
    path("", include("misago.auth.urls")),
    path("", include("misago.legal.urls")),
    path("", include("misago.users.urls")),
    path("account/", include("misago.account.urls")),
    path("", include("misago.attachments.urls")),
    path("", include("misago.categories.urls")),
    path("", include("misago.polls.urls")),
    path("", include("misago.posting.urls")),
    path("", include("misago.threads.urls")),
    path("", include("misago.privatethreads.urls")),
    path("", include("misago.edits.urls")),
    path("", include("misago.likes.urls")),
    path("", include("misago.threadupdates.urls")),
    path("", include("misago.notifications.urls")),
    path("", include("misago.search.urls")),
    path("", include("misago.oauth2.urls")),
    path("", include("misago.socialauth.urls")),
    path("formatting-help/", formatting_help, name="formatting-help"),
    path("", include("misago.healthcheck.urls")),
    # default robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(
            content_type="text/plain", template_name="misago/robots.txt"
        ),
    ),
    # "misago:index" link symbolises "root" of Misago links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago and will be handled by misago.views.exceptionhandler if it
    # results in Http404 or PermissionDenied exception
    path("", forum_index, name="index"),
]


# Register API
apipatterns = hooks.apipatterns + [
    path("", include("misago.legal.urls.api")),
    path("", include("misago.markup.urls")),
    path("", include("misago.users.urls.api")),
    path("", include("misago.search.urls.api")),
]

urlpatterns += [
    path("api/", include((apipatterns, "api"), namespace="api")),
    path("api/v2/", include("misago.apiv2.urls")),
]


# Register Misago ACP
if settings.MISAGO_ADMIN_PATH:
    # Admin patterns recognised by Misago
    adminpatterns = [path("", include("misago.admin.urls"))]

    admin_prefix = f"{settings.MISAGO_ADMIN_PATH}/"
    urlpatterns += [
        path(admin_prefix, include((adminpatterns, "admin"), namespace="admin"))
    ]
