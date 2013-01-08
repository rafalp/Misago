from django.conf import settings
from django.conf.urls import include, patterns, url

urlpatterns = []
for extension in settings.USERCP_EXTENSIONS:
    urlpatterns += patterns('',
        (r'^', include(extension + '.urls')),
    )
