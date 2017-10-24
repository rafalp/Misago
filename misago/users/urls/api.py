from django.conf.urls import url

from misago.api.router import MisagoApiRouter
from misago.users.api import auth, captcha, mention
from misago.users.api.ranks import RanksViewSet
from misago.users.api.usernamechanges import UsernameChangesViewSet
from misago.users.api.users import UserViewSet


urlpatterns = [
    url(r'^auth/$', auth.gateway, name='auth'),
    url(r'^auth/requirements/$', auth.get_requirements, name='auth-requirements'),
    url(r'^auth/send-activation/$', auth.send_activation, name='send-activation'),
    url(r'^auth/send-password-form/$', auth.send_password_form, name='send-password-form'),
    url(r'^auth/change-password/(?P<pk>\d+)/', auth.change_forgotten_password, name='change-forgotten-password'),
    url(r'^captcha-question/$', captcha.question, name='captcha-question'),
    url(r'^mention/$', mention.mention_suggestions, name='mention-suggestions'),
]

router = MisagoApiRouter()
router.register(r'ranks', RanksViewSet)
router.register(r'users', UserViewSet)
router.register(r'username-changes', UsernameChangesViewSet, base_name='usernamechange')
urlpatterns += router.urls
