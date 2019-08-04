from django.contrib.auth import get_user_model
from django.http import Http404
from simple_sso.sso_client.client import AuthenticateView, Client, LoginView

from ..users.authbackends import MisagoBackend
from ..users.setupnewuser import setup_new_user

User = get_user_model()


class MisagoAuthenticateView(AuthenticateView):
    @property
    def client(self):
        return create_configured_client(self.request)

    def get(self, request):
        if not request.settings.enable_sso:
            raise Http404()

        return super().get(request)


class MisagoLoginView(LoginView):
    @property
    def client(self):
        return create_configured_client(self.request)

    def get(self, request):
        if not request.settings.enable_sso:
            raise Http404()

        return super().get(request)


def create_configured_client(request):
    settings = request.settings

    return ClientMisago(
        settings.sso_server,
        settings.sso_public_key,
        settings.sso_private_key,
        request=request,
    )


class ClientMisago(Client):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.backend = "%s.%s" % (MisagoBackend.__module__, MisagoBackend.__name__)

    def build_user(self, user_data):
        try:
            return User.objects.get_by_email(user_data["email"])
        except User.DoesNotExist:
            user = User.objects.create_user(user_data["username"], user_data["email"])
            user.update_acl_key()
            setup_new_user(self.request.settings, user)
            return user
