from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


def admin_login(client, username, password):
    client.post(reverse('misago:admin:index'),
                data={'username': username, 'password': password})


class AdminTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser('TestAdmin', 'admin@test.com', 'Pass.123')
        admin_login(self.client, 'TestAdmin', 'Pass.123')
