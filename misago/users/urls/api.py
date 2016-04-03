from django.conf.urls import patterns, url
from misago.core.apirouter import MisagoApiRouter
from misago.users.api.ranks import RanksViewSet
from misago.users.api.users import UserViewSet
from misago.users.api.usernamechanges import UsernameChangesViewSet


urlpatterns = patterns('misago.users.api.auth',
    url(r'^auth/$', 'gateway', name='auth'),
    url(r'^auth/send-activation/$', 'send_activation', name='send-activation'),
    url(r'^auth/send-password-form/$', 'send_password_form', name='send-password-form'),
    url(r'^auth/change-password/(?P<pk>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'change_forgotten_password', name='change-forgotten-password'),
)

urlpatterns += patterns('misago.users.api.captcha',
    url(r'^captcha-question/$', 'question', name='captcha-question'),
)

router = MisagoApiRouter()
router.register(r'ranks', RanksViewSet)
router.register(r'users', UserViewSet)
router.register(r'username-changes', UsernameChangesViewSet, base_name='usernamechange')
urlpatterns += router.urls
