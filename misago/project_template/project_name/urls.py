from django.conf import settings
from django.conf.urls import patterns, include, url

# Setup Django admin to work with Misago auth
from django.contrib import admin
from misago.users.forms.auth import AdminAuthenticationForm
admin.autodiscover()
admin.site.login_form = AdminAuthenticationForm

urlpatterns = patterns('',
    url(r'^', include('misago.urls', namespace='misago')),

    # Javascript translations
    url(r'^django-i18n.js$', 'misago.core.views.javascript_catalog'),
    url(r'^moment-i18n.js$', 'misago.core.views.momentjs_catalog'),

    # In-dev preload data for Ember-CLI
    url(r'^misago-preload-data.js$', 'misago.core.views.preload_data'),

    # Uncomment next line if you plan to use Django admin for 3rd party apps
    #url(r'^django-admin/', include(admin.site.urls)),

    # Uncomment next line if you plan to use browseable API
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)


# Serve static and media files in development
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Error Handlers
# Misago needs those handlers to deal with errors raised by it's middlewares
# If you replace those handlers with custom ones, make sure you decorate them
# functions with shared_403_exception_handler or shared_404_exception_handler
# decorators that are defined in misago.views.errorpages module!
handler403 = 'misago.core.errorpages.permission_denied'
handler404 = 'misago.core.errorpages.page_not_found'
