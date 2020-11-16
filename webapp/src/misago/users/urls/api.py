from django.conf.urls import url

from ...core.apirouter import MisagoApiRouter
from ..api import auth, captcha, mention
from ..api.ranks import RanksViewSet
from ..api.usernamechanges import UsernameChangesViewSet
from ..api.users import UserViewSet

urlpatterns = [
    url(r"^auth/$", auth.gateway, name="auth"),
    url(r"^auth/criteria/$", auth.get_criteria, name="auth-criteria"),
    url(r"^auth/send-activation/$", auth.send_activation, name="send-activation"),
    url(
        r"^auth/send-password-form/$",
        auth.send_password_form,
        name="send-password-form",
    ),
    url(
        r"^auth/change-password/(?P<pk>\d+)/(?P<token>[a-zA-Z0-9]+)/$",
        auth.change_forgotten_password,
        name="change-forgotten-password",
    ),
    url(r"^captcha-question/$", captcha.question, name="captcha-question"),
    url(r"^mention/$", mention.mention_suggestions, name="mention-suggestions"),
]

router = MisagoApiRouter()
router.register(r"ranks", RanksViewSet)
router.register(r"users", UserViewSet)
router.register(r"username-changes", UsernameChangesViewSet, basename="usernamechange")
urlpatterns += router.urls
