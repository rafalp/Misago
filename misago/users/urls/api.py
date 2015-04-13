from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
from misago.users.api.users import UserViewSet


urlpatterns = patterns('misago.users.api.auth',
    url(r'^login/$', 'login', name='login'),
)

urlpatterns += patterns('misago.users.api.activation',
    url(r'^activation/send-link/$', 'send_link', name="activation_send_link"),
    url(r'^activation/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/validate-token/$', 'validate_token', name="activation_validate_token"),
)

urlpatterns += patterns('misago.users.api.changepassword',
    url(r'^change-password/send-link/$', 'send_link', name='change_password_send_link'),
    url(r'^change-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/validate-token/$', 'validate_token', name='change_password_validate_token'),
    url(r'^change-password/(?P<user_id>\d+)/(?P<token>[a-zA-Z0-9]+)/$', 'change_password', name='change_password'),
)

urlpatterns = patterns('misago.users.api.captcha',
    url(r'^captcha-questions/(?P<question_id>\d+)/$', 'question', name='captcha_question'),
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns += router.urls
