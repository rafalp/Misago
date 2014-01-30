from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('misago.urls')),
    # Uncomment next line if you plan to use Django admin for 3rd party apps
    #url(r'^django-admin/', include(admin.site.urls)),
)


# Error Handlers
# Misago needs those handlers to deal with errors raised by it's middlewares
# If you replace those handlers with custom ones, make sure you decorate them
# functions with shared_403_exception_handler or shared_404_exception_handler
# decorators that are defined in misago.views.errorpages module!
handler403 = 'misago.views.errorpages.permission_denied'
handler404 = 'misago.views.errorpages.page_not_found'


# Serve static files in development
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
