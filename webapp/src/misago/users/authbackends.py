from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class MisagoBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get("email"):
            username = kwargs["email"]  # Bias to email if it was passed explictly

        if not username or not password:
            # If no username or password was given, skip rest of this auth
            # This may happen if we are during different auth flow (eg. OAuth/JWT)
            return None

        try:
            user = User.objects.get_by_username_or_email(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, pk):
        try:
            manager = User._default_manager
            relations = ("rank", "online_tracker", "ban_cache")
            user = manager.select_related(*relations).get(pk=pk)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
