from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase

from misago.conf.models import SettingsGroup


class AdminSettingsViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin index view contains settings link"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertIn(reverse('misago:admin:settings:index'), response.content)

    def test_groups_list_view(self):
        """settings group view returns 200 and contains all settings groups"""
        response = self.client.get(reverse('misago:admin:settings:index'))

        self.assertEqual(response.status_code, 200)
        for group in SettingsGroup.objects.all():
            group_link = reverse('misago:admin:settings:group', kwargs={
                'key': group.key
            })
            self.assertIn(group.name, response.content)
            self.assertIn(group_link, response.content)

    def test_groups_views(self):
        """
        each settings group view returns 200 and contains all settings in group
        """
        for group in SettingsGroup.objects.all():
            group_link = reverse('misago:admin:settings:group', kwargs={
                'key': group.key
            })
            response = self.client.get(group_link)

            self.assertEqual(response.status_code, 200)
            self.assertIn(group.name, response.content)

            values = {}
            for setting in group.setting_set.all():
                values[setting.setting] = setting.value
                self.assertIn(setting.name, response.content)

            response = self.client.post(group_link, data=values)
            self.assertEqual(response.status_code, 302)
