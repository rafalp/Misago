from django.urls import include, path

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
    path("", include("social_django.urls", namespace="social")),
    path("forum/", include("misago.urls", namespace="misago")),
    path("django-admin/", admin.site.urls),
    path(
        "django-i18n.js",
        cache_page(86400 * 2, key_prefix="misagojsi18n")(
            last_modified(lambda req, **kw: timezone.now())(
                JavaScriptCatalog.as_view(packages=["misago"])
            )
        ),
        name="django-i18n",
    ),
    path("forum/test-pagination/", views.test_pagination, name="test-pagination"),
    path(
        "forum/test-pagination/<int:page>/",
        views.test_pagination,
        name="test-pagination",
    ),
    path(
        "forum/test-paginated-response/",
        views.test_paginated_response,
        name="test-paginated-response",
    ),
    path(
        "forum/test-paginated-response-data/",
        views.test_paginated_response_data,
        name="test-paginated-response-data",
    ),
    path(
        "forum/test-paginated-response-serializer/",
        views.test_paginated_response_serializer,
        name="test-paginated-response-serializer",
    ),
    path(
        "forum/test-paginated-response-data-serializer/",
        views.test_paginated_response_data_serializer,
        name="test-paginated-response-data-serializer",
    ),
    path(
        "forum/test-paginated-response-data-extra/",
        views.test_paginated_response_data_extra,
        name="test-paginated-response-data-extra",
    ),
    path(
        "forum/test-valid-slug/<slug:slug>-<int:pk>/",
        views.validate_slug_view,
        name="validate-slug-view",
    ),
    path("forum/test-banned/", views.raise_misago_banned, name="raise-misago-banned"),
    path("forum/test-403/", views.raise_misago_403, name="raise-misago-403"),
    path("forum/test-404/", views.raise_misago_404, name="raise-misago-404"),
    path("forum/test-405/", views.raise_misago_405, name="raise-misago-405"),
    path(
        "forum/social-auth-failed/",
        views.raise_social_auth_failed,
        name="raise-social-auth-failed",
    ),
    path(
        "forum/social-wrong-backend/",
        views.raise_social_wrong_backend,
        name="raise-social-wrong-backend",
    ),
    path(
        "forum/social-not-allowed-to-disconnect/",
        views.raise_social_not_allowed_to_disconnect,
        name="raise-social-not-allowed-to-disconnect",
    ),
    path(
        "forum/raise-social-auth-failed-message/",
        views.raise_social_auth_failed_message,
        name="raise-social-auth-failed-message",
    ),
    path(
        "forum/raise-social-auth-banned/",
        views.raise_social_auth_banned,
        name="raise-social-auth-banned",
    ),
    path("test-403/", views.raise_403, name="raise-403"),
    path("test-404/", views.raise_404, name="raise-404"),
    path("test-redirect/", views.test_redirect, name="test-redirect"),
    path("test-require-post/", views.test_require_post, name="test-require-post"),
]
