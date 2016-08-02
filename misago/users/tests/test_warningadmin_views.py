from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase

from ..models import WarningLevel


class WarningsAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains warning levels link"""
        response = self.client.get(
            reverse('misago:admin:users:accounts:index'))

        response = self.client.get(response['location'])
        self.assertContains(response, reverse('misago:admin:users:warnings:index'))

    def test_list_view(self):
        """warning levels list view returns 200"""
        response = self.client.get(
            reverse('misago:admin:users:warnings:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No warning levels')

    def test_new_view(self):
        """new warning level view has no showstoppers"""
        response = self.client.get(
            reverse('misago:admin:users:warnings:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Test Level',
                'length_in_minutes': 60,
                'restricts_posting_replies': '1',
                'restricts_posting_threads': '1',
            })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:admin:users:warnings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Level')

    def test_edit_view(self):
        """edit warning level view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Test Level',
                'length_in_minutes': 60,
                'restricts_posting_replies': '1',
                'restricts_posting_threads': '1',
            })

        test_level = WarningLevel.objects.get(level=1)

        response = self.client.get(
            reverse('misago:admin:users:warnings:edit',
                    kwargs={'pk': test_level.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_level.name)

        response = self.client.post(
            reverse('misago:admin:users:warnings:edit',
                    kwargs={'pk': test_level.pk}),
            data={
                'name': 'Edited Level',
                'length_in_minutes': 5,
                'restricts_posting_replies': '0',
                'restricts_posting_threads': '0',
            })
        self.assertEqual(response.status_code, 302)

        test_level = WarningLevel.objects.get(level=1)
        response = self.client.get(
            reverse('misago:admin:users:warnings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_level.name)
        self.assertNotContains(response, 'Test Level')

    def test_move_up_view(self):
        """move warning level up view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Level 1',
                'length_in_minutes': 5,
                'restricts_posting_replies': '0',
                'restricts_posting_threads': '0',
            })
        self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Level 2',
                'length_in_minutes': 5,
                'restricts_posting_replies': '0',
                'restricts_posting_threads': '0',
            })

        test_level_1 = WarningLevel.objects.get(level=1)
        test_level_2 = WarningLevel.objects.get(level=2)

        response = self.client.post(
            reverse('misago:admin:users:warnings:up',
                    kwargs={'pk': test_level_2.pk}))
        self.assertEqual(response.status_code, 302)

        changed_level_1 = WarningLevel.objects.get(id=test_level_1.pk)
        changed_level_2 = WarningLevel.objects.get(id=test_level_2.pk)
        self.assertEqual(test_level_1.level, changed_level_2.level)
        self.assertEqual(test_level_2.level, changed_level_1.level)

    def test_move_down_view(self):
        """move warning level down view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Level 1',
                'length_in_minutes': 5,
                'restricts_posting_replies': '0',
                'restricts_posting_threads': '0',
            })
        self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Level 2',
                'length_in_minutes': 5,
                'restricts_posting_replies': '0',
                'restricts_posting_threads': '0',
            })

        test_level_1 = WarningLevel.objects.get(level=1)
        test_level_2 = WarningLevel.objects.get(level=2)

        response = self.client.post(
            reverse('misago:admin:users:warnings:down',
                    kwargs={'pk': test_level_1.pk}))
        self.assertEqual(response.status_code, 302)

        changed_level_1 = WarningLevel.objects.get(id=test_level_1.pk)
        changed_level_2 = WarningLevel.objects.get(id=test_level_2.pk)
        self.assertEqual(test_level_1.level, changed_level_2.level)
        self.assertEqual(test_level_2.level, changed_level_1.level)

    def test_delete_view(self):
        """delete warning level view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:warnings:new'),
            data={
                'name': 'Test Level',
                'length_in_minutes': 60,
                'restricts_posting_replies': '1',
                'restricts_posting_threads': '1',
            })

        test_level = WarningLevel.objects.get(level=1)

        response = self.client.post(
            reverse('misago:admin:users:warnings:delete',
                    kwargs={'pk': test_level.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.get(reverse('misago:admin:users:warnings:index'))
        response = self.client.get(
            reverse('misago:admin:users:warnings:index'))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, test_level.name)
