from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from misago.admin.testutils import admin_login
from misago.admin.views import get_protected_namespace
from misago.conf.models import SettingsGroup


class AdminSettingsViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_superuser('Bob', 'bob@test.com', 'Pass.123')
        admin_login(self.client, 'Bob', 'Pass.123')

    def test_link_registered(self):
        """admin index view contains settings link"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertIn(reverse('misago:admin:settings:index'), response.content)

    def test_groups_list_view(self):
        """settings group view returns 200 and contains all settings groups"""
        response = self.client.get(reverse('misago:admin:settings:index'))

        self.assertEqual(response.status_code, 200)
        for group in SettingsGroup.objects.all():
            group_link = reverse('misago:admin:settings:group',
                                 kwargs={'group_key': group.key})
            self.assertIn(group.name, response.content)
            self.assertIn(group_link, response.content)

    def test_groups_views(self):
        """
        each settings group view returns 200 and contains all settings in group
        """
        for group in SettingsGroup.objects.all():
            group_link = reverse('misago:admin:settings:group',
                                 kwargs={'group_key': group.key})
            response = self.client.get(group_link)

            self.assertEqual(response.status_code, 200)
            self.assertIn(group.name, response.content)

            for setting in group.setting_set.all():
                self.assertIn(setting.name, response.content)

