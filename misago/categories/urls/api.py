from django.conf.urls import patterns, url


urlpatterns = patterns('misago.categories.views',
    url(r'^categories/$', 'api', name='categories'),
)