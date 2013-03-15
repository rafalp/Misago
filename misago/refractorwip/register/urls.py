from django.conf.urls import patterns, url

urlpatterns = patterns('misago.register.views',
    url(r'^$', 'form', name="register"),
)