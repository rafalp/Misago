from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from misago.conf import settings
from misago.conf.shortcuts import get_dynamic_settings
from misago.users.authbackends import MisagoBackend
from misago.users.setupnewuser import setup_new_user

from simple_sso.sso_client.client import Client

User = get_user_model()


class ClientMisago(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = "%s.%s" % (MisagoBackend.__module__, MisagoBackend.__name__)

    def build_user(self, user_data):
        try:
            user = User.objects.get(username=user_data['username'])
        except User.DoesNotExist:

            # TODO: Check. Is user_data safe?
            user = User.objects.create_user(
                user_data["username"],
                user_data["email"],
                make_password(make_password('ItDoesMatter')),
            )

            user.update_acl_key()

            user_settings = get_dynamic_settings()
            setup_new_user(user_settings, user)

        return user


client = ClientMisago(settings.SSO_SERVER, settings.SSO_PUBLIC_KEY, settings.SSO_PRIVATE_KEY)
