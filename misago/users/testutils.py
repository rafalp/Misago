from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import AnonymousUser


class UserTestCase(TestCase):
    USER_PASSWORD = "Pass.123"

    def setUp(self):
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

    def login_user(self, user):
        self.client.post(reverse('misago:api:login'), data={
            'username': user.email,
            'password': self.USER_PASSWORD,
        })
        self.client.get(reverse('misago:index'))

    def logout_user(self):
        self.client.post(reverse('misago:logout'))
        self.client.get(reverse('misago:index'))


class AuthenticatedUserTestCase(UserTestCase):
    def setUp(self):
        self.user = self.get_authenticated_user()
        self.login_user(self.user)

    def reload_user(self):
        User = get_user_model()
        self.user = User.objects.get(id=self.user.id)


class SuperUserTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        self.user = self.get_superuser()
        self.login_user(self.user)
