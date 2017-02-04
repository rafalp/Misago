"""{{ project_name }} URL Configuration

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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from misago.core.views import javascript_catalog
from misago.users.forms.auth import AdminAuthenticationForm


admin.autodiscover()
admin.site.login_form = AdminAuthenticationForm


urlpatterns = [
    url(r'^', include('misago.urls', namespace='misago')),

    # Javascript translations
    url(r'^django-i18n.js$', javascript_catalog, name='django-i18n'),

    # Uncomment next line if you plan to use Django admin for 3rd party apps
    #url(r'^django-admin/', include(admin.site.urls)),
]


# If debug mode is enabled, include debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


# Use static file server for static and media files (debug only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Error Handlers
# Misago needs those handlers to deal with errors raised by it's middlewares
# If you replace those handlers with custom ones, make sure you decorate them
# with shared_403_exception_handler or shared_404_exception_handler
# decorators that are defined in misago.views.errorpages module!
handler403 = 'misago.core.errorpages.permission_denied'
handler404 = 'misago.core.errorpages.page_not_found'
