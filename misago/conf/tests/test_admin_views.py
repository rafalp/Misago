from django.urls import reverse

from misago.admin.testutils import AdminTestCase
from misago.conf.models import SettingsGroup


class AdminSettingsViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin index view contains settings link"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, reverse('misago:admin:system:settings:index'))

    def test_groups_list_view(self):
        """settings group view returns 200 and contains all settings groups"""
        response = self.client.get(reverse('misago:admin:system:settings:index'))

        self.assertEqual(response.status_code, 200)
        for group in SettingsGroup.objects.all():
            group_link = reverse(
                'misago:admin:system:settings:group', kwargs={
                    'key': group.key,
                }
            )
            self.assertContains(response, group.name)
            self.assertContains(response, group_link)

    def test_invalid_group_handling(self):
        """invalid group results in redirect to settings list"""
        group_link = reverse(
            'misago:admin:system:settings:group', kwargs={
                'key': 'invalid-group',
            }
        )
        response = self.client.get(group_link)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('misago:admin:system:settings:index') in response['location'])

    def test_groups_views(self):
        """each settings group view returns 200 and contains all settings in group"""
        for group in SettingsGroup.objects.all():
            group_link = reverse(
                'misago:admin:system:settings:group', kwargs={
                    'key': group.key,
                }
            )
            response = self.client.get(group_link)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, group.name)

            values = {}
            for setting in group.setting_set.all():
                values[setting.setting] = setting.value
                self.assertContains(response, setting.name)

            response = self.client.post(group_link, data=values)
            self.assertEqual(response.status_code, 302)
