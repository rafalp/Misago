from django.conf import settings
from django.conf.urls import include, patterns, url
from django.utils.importlib import import_module

urlpatterns = []
iteration = 0
for extension in settings.USERCP_EXTENSIONS:
    iteration += 1
    usercp_module = import_module(extension + '.urls')
    try:
        urlpatterns += patterns('',
            (r'^', include(usercp_module.register_usercp_urls(iteration == 1))),
        )
    except AttributeError:
        pass
