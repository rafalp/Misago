from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.core.testutils import MisagoTestCase

from .models import AnonymousUser, Online


class UserTestCase(MisagoTestCase):
    USER_PASSWORD = "Pass.123"

    def setUp(self):
        super(UserTestCase, self).setUp()
        self.get_initial_user()

    def get_initial_user(self):
        self.user = self.get_anonymous_user()

    def get_anonymous_user(self):
        return AnonymousUser()

    def get_authenticated_user(self):
        User = get_user_model()
        return User.objects.create_user(
            "TestUser", "test@user.com", self.USER_PASSWORD)

    def get_superuser(self):
        User = get_user_model()
        return User.objects.create_superuser(
            "TestSuperUser", "test@superuser.com", self.USER_PASSWORD)

    def login_user(self, user, password=None):
        self.client.force_login(user)

    def logout_user(self):
        if self.user.is_authenticated:
            Online.objects.filter(user=self.user).delete()
        self.client.logout()


class AuthenticatedUserTestCase(UserTestCase):
    def get_initial_user(self):
        self.user = self.get_authenticated_user()
        self.login_user(self.user)

    def reload_user(self):
        User = get_user_model()
        self.user = User.objects.get(id=self.user.id)


class SuperUserTestCase(AuthenticatedUserTestCase):
    def get_initial_user(self):
        self.user = self.get_superuser()
        self.login_user(self.user)
