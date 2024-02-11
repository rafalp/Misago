"""devproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from misago import __released__, __version__
from misago.plugins.urlpatterns import discover_plugins_urlpatterns
from misago.users.forms.auth import AdminAuthenticationForm


# Cache key for django-i18n.js view that invalidates cache when
# Misago version, release status or language code changes
misago_i18n_cache_key = (
    (f"misagojsi18n_{settings.LANGUAGE_CODE}_{__version__}_{__released__}")
    .replace(".", "_")
    .replace("-", "_")
    .lower()
)


admin.autodiscover()
admin.site.login_form = AdminAuthenticationForm


urlpatterns = discover_plugins_urlpatterns(settings.INSTALLED_PLUGINS) + [
    path("", include("misago.urls", namespace="misago")),
    # Javascript translations
    path(
        "django-i18n.js",
        last_modified(lambda req, **kw: timezone.now())(
            cache_page(86400 * 21, key_prefix=misago_i18n_cache_key)(
                JavaScriptCatalog.as_view(packages=["misago"])
            )
        ),
        name="django-i18n",
    ),
    # Uncomment next line if you plan to use Django admin for 3rd party apps
    path("django-admin/", admin.site.urls),
]


# If debug mode is enabled, include debug toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]


# Use static file server for static and media files (debug only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Error Handlers
# Misago needs those handlers to deal with errors raised by it's middlewares
# If you replace those handlers with custom ones, make sure you decorate them
# with shared_403_exception_handler or shared_404_exception_handler
# decorators that are defined in misago.views.errorpages module!
handler403 = "misago.core.errorpages.permission_denied"
handler404 = "misago.core.errorpages.page_not_found"
