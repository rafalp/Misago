from django.conf import settings
from django.conf.urls import patterns, url


if settings.MISAGO_CATEGORIES_ON_INDEX:
    URL_PATH = r'^$'
else:
    URL_PATH = r'^categories/$'


urlpatterns = patterns('misago.categories.views',
    url(URL_PATH, 'categories', name='categories'),
)


# fallback for after we changed index setting
urlpatterns += patterns('misago.core.views',
    url(r'^categories/$', 'home_redirect'),
)