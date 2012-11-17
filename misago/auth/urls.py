from django.conf.urls import patterns, url, include

urlpatterns = patterns('misago.auth.views',
    url(r'^register/$', 'register', name="register"),
    url(r'^activate/(?P<username>\w+)-(?P<user>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activate', name="activate"),
    url(r'^resend-activation/$', 'send_activation', name="send_activation"),
    url(r'^reset-pass/$', 'forgot_password', name="forgot_password"),
    url(r'^reset-pass/(?P<username>\w+)-(?P<user>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'reset_password', name="reset_password"),
)