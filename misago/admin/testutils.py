from django.core.urlresolvers import reverse

from misago.users.testutils import SuperUserTestCase


class AdminTestCase(SuperUserTestCase):
    def setUp(self):
        self.user = self.get_superuser()
        self.login_admin(self.user)

    def login_admin(self, user):
        self.client.post(reverse('misago:admin:index'), data={
            'username': user.email,
            'password': self.USER_PASSWORD
        })
        self.client.get(reverse('misago:admin:index'))
