from django.urls import path

from ...core.apirouter import MisagoApiRouter
from ..api import auth, captcha, mention
from ..api.ranks import RanksViewSet
from ..api.usernamechanges import UsernameChangesViewSet
from ..api.users import UserViewSet

urlpatterns = [
    path("auth/", auth.gateway, name="auth"),
    path("auth/criteria/", auth.get_criteria, name="auth-criteria"),
    path("auth/send-activation/", auth.send_activation, name="send-activation"),
    path(
        "auth/send-password-form/",
        auth.send_password_form,
        name="send-password-form",
    ),
    path(
        "auth/change-password/<int:pk>/<slug:token>/",
        auth.change_forgotten_password,
        name="change-forgotten-password",
    ),
    path("captcha-question/", captcha.question, name="captcha-question"),
    path("mention/", mention.mention_suggestions, name="mention-suggestions"),
]

router = MisagoApiRouter()
router.register(r"ranks", RanksViewSet)
router.register(r"users", UserViewSet)
router.register(r"username-changes", UsernameChangesViewSet, basename="usernamechange")
urlpatterns += router.urls
