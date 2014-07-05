from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class MisagoBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel.objects.get_by_username_or_email(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            manager = UserModel._default_manager
            relations = ('online_tracker', 'ban_cache')
            return manager.select_related(*relations).get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
