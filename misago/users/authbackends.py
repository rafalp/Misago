from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


UserModel = get_user_model()


class MisagoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel.objects.get_by_username_or_email(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, pk):
        try:
            manager = UserModel._default_manager
            relations = ('rank', 'online_tracker', 'ban_cache')
            user = manager.select_related(*relations).get(pk=pk)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
