from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
from misago.users.api.users import UserViewSet


urlpatterns = patterns('misago.users.api.auth',
    url(r'^auth/$', 'gateway'),
    url(r'^auth/send-activation/$', 'send_activation'),
    url(r'^auth/activate-account/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'activate_account'),
    url(r'^auth/send-password-form/$', 'send_password_form'),
    url(r'^auth/change-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'change_forgotten_password'),
)

urlpatterns += patterns('misago.users.api.captcha',
    url(r'^captcha-questions/(?P<question_id>\d+)/$', 'question', name='captcha_question'),
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns += router.urls
