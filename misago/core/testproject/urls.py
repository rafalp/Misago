from django.conf.urls import include, url

# Setup Django admin to work with Misago auth
from django.contrib import admin
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from . import views
from ...users.forms.auth import AdminAuthenticationForm

admin.autodiscover()
admin.site.login_form = AdminAuthenticationForm

urlpatterns = [
    url(r"^", include("social_django.urls", namespace="social")),
    url(r"^forum/", include("misago.urls", namespace="misago")),
    url(r"^django-admin/", admin.site.urls),
    url(
        r"^django-i18n.js$",
        cache_page(86400 * 2, key_prefix="misagojsi18n")(
            last_modified(lambda req, **kw: timezone.now())(
                JavaScriptCatalog.as_view(packages=["misago"])
            )
        ),
        name="django-i18n",
    ),
    # django-simple-sso doesn't have namespaces, we can't use namespace here
    url(r"^sso/", include("misago.sso.urls")),
    url(r"^forum/test-pagination/$", views.test_pagination, name="test-pagination"),
    url(
        r"^forum/test-pagination/(?P<page>[1-9][0-9]*)/$",
        views.test_pagination,
        name="test-pagination",
    ),
    url(
        r"^forum/test-paginated-response/$",
        views.test_paginated_response,
        name="test-paginated-response",
    ),
    url(
        r"^forum/test-paginated-response-data/$",
        views.test_paginated_response_data,
        name="test-paginated-response-data",
    ),
    url(
        r"^forum/test-paginated-response-serializer/$",
        views.test_paginated_response_serializer,
        name="test-paginated-response-serializer",
    ),
    url(
        r"^forum/test-paginated-response-data-serializer/$",
        views.test_paginated_response_data_serializer,
        name="test-paginated-response-data-serializer",
    ),
    url(
        r"^forum/test-paginated-response-data-extra/$",
        views.test_paginated_response_data_extra,
        name="test-paginated-response-data-extra",
    ),
    url(
        r"^forum/test-valid-slug/(?P<slug>[a-z0-9\-]+)-(?P<pk>\d+)/$",
        views.validate_slug_view,
        name="validate-slug-view",
    ),
    url(r"^forum/test-banned/$", views.raise_misago_banned, name="raise-misago-banned"),
    url(r"^forum/test-403/$", views.raise_misago_403, name="raise-misago-403"),
    url(r"^forum/test-404/$", views.raise_misago_404, name="raise-misago-404"),
    url(r"^forum/test-405/$", views.raise_misago_405, name="raise-misago-405"),
    url(
        r"^forum/social-auth-failed/$",
        views.raise_social_auth_failed,
        name="raise-social-auth-failed",
    ),
    url(
        r"^forum/social-wrong-backend/$",
        views.raise_social_wrong_backend,
        name="raise-social-wrong-backend",
    ),
    url(
        r"^forum/social-not-allowed-to-disconnect/$",
        views.raise_social_not_allowed_to_disconnect,
        name="raise-social-not-allowed-to-disconnect",
    ),
    url(
        r"^forum/raise-social-auth-failed-message/$",
        views.raise_social_auth_failed_message,
        name="raise-social-auth-failed-message",
    ),
    url(
        r"^forum/raise-social-auth-banned/$",
        views.raise_social_auth_banned,
        name="raise-social-auth-banned",
    ),
    url(r"^test-403/$", views.raise_403, name="raise-403"),
    url(r"^test-404/$", views.raise_404, name="raise-404"),
    url(r"^test-redirect/$", views.test_redirect, name="test-redirect"),
    url(r"^test-require-post/$", views.test_require_post, name="test-require-post"),
]
