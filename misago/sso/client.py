from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from misago.conf import settings
from simple_sso.sso_client.client import Client

User = get_user_model()


class ClientMisago(Client):
    def build_user(self, user_data):
        try:
            user = User.objects.get(username=user_data['username'])
        except User.DoesNotExist:

            # TODO: Check. Is user_data safe?
            user = User.objects.create_user(
                user_data["username"],
                user_data["email"],
                make_password(None),
            )

            user.update_acl_key()

        return user


client = ClientMisago(settings.SSO_SERVER, settings.SSO_PUBLIC_KEY, settings.SSO_PRIVATE_KEY)
