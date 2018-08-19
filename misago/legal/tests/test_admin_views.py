from django.urls import reverse

from misago.admin.testutils import AdminTestCase
from misago.legal.models import Agreement


class AgreementAdminViewsTests(AdminTestCase):
    def test_link_registered(self):
        """admin nav contains agreements link"""
        response = self.client.get(reverse('misago:admin:users:accounts:index'))

        response = self.client.get(response['location'])
        self.assertContains(response, reverse('misago:admin:users:agreements:index'))

    def test_list_view(self):
        """agreements list view returns 200"""
        response = self.client.get(reverse('misago:admin:users:agreements:index'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)

    def test_mass_delete(self):
        """adminview deletes multiple agreements"""
        for i in range(10):
            response = self.client.post(
                reverse('misago:admin:users:agreements:new'),
                data={
                    'type': Agreement.TYPE_TOS,
                    'text': 'test agreement!',
                },
            )
            self.assertEqual(response.status_code, 302)

        self.assertEqual(Agreement.objects.count(), 10)

        agreements_pks = []
        for agreement in Agreement.objects.iterator():
            agreements_pks.append(agreement.pk)

        response = self.client.post(
            reverse('misago:admin:users:agreements:index'),
            data={
                'action': 'delete',
                'selected_items': agreements_pks,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Agreement.objects.count(), 0)

    def test_new_view(self):
        """new agreement view has no showstoppers"""
        response = self.client.get(reverse('misago:admin:users:agreements:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Test Rules',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:users:agreements:index'))
        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Rules')

        test_agreement = Agreement.objects.get(type=Agreement.TYPE_TOS)
        self.assertIsNone(test_agreement.last_modified_on)
        self.assertIsNone(test_agreement.last_modified_by)
        self.assertIsNone(test_agreement.last_modified_by_name)

    def test_new_view_change_active(self):
        """new agreement view creates new active agreement"""
        response = self.client.get(reverse('misago:admin:users:agreements:new'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Old Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'New Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
                'is_active': True,
            },
        )
        self.assertEqual(response.status_code, 302)

        test_agreement = Agreement.objects.get(is_active=True)
        self.assertEqual(test_agreement.title, 'New Active')

    def test_edit_view(self):
        """edit agreement view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Test Rules',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )

        test_agreement = Agreement.objects.get(type=Agreement.TYPE_TOS)
        form_link = reverse(
            'misago:admin:users:agreements:edit',
            kwargs={
                'pk': test_agreement.pk,
            },
        )

        response = self.client.post(
            form_link,
            data={
                'type': Agreement.TYPE_PRIVACY,
                'title': 'Test Privacy',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:users:agreements:index'))
        response = self.client.get(response['location'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Privacy')

        updated_agreement = Agreement.objects.get(type=Agreement.TYPE_PRIVACY)
        self.assertTrue(updated_agreement.last_modified_on)
        self.assertEqual(updated_agreement.last_modified_by, self.user)
        self.assertEqual(updated_agreement.last_modified_by_name, self.user.username)

    def test_edit_view_change_active(self):
        """edit agreement view sets new active"""
        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Old Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
                'is_active': True
            },
        )

        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'New Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )

        test_agreement = Agreement.objects.get(title='New Active')
        form_link = reverse(
            'misago:admin:users:agreements:edit',
            kwargs={
                'pk': test_agreement.pk,
            },
        )

        response = self.client.post(
            form_link,
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Updated Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
                'is_active': True
            },
        )
        self.assertEqual(response.status_code, 302)

        updated_agreement = Agreement.objects.get(is_active=True)
        self.assertEqual(updated_agreement.title, 'Updated Active')

    def test_delete_view(self):
        """delete agreement view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Test Rules',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )

        test_agreement = Agreement.objects.get(type=Agreement.TYPE_TOS)

        response = self.client.post(
            reverse(
                'misago:admin:users:agreements:delete',
                kwargs={
                    'pk': test_agreement.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:users:agreements:index'))
        self.client.get(response['location'])
        response = self.client.get(response['location'])

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, test_agreement.title)

    def test_set_as_active_view(self):
        """set agreement as active view has no showstoppers"""
        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Test Rules',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )

        test_agreement = Agreement.objects.get(type=Agreement.TYPE_TOS)

        response = self.client.post(
            reverse(
                'misago:admin:users:agreements:set-as-active',
                kwargs={
                    'pk': test_agreement.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 302)

        updated_agreement = Agreement.objects.get(is_active=True)
        self.assertEqual(updated_agreement, test_agreement)

    def test_set_as_active_view_change_active(self):
        """set agreement as active view changes current active"""
        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'Old Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
                'is_active': True,
            },
        )

        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'title': 'New Active',
                'text': 'Lorem ipsum dolor met sit amet elit',
                'link': 'https://example.com/rules/',
            },
        )

        test_agreement = Agreement.objects.get(title='New Active')

        response = self.client.post(
            reverse(
                'misago:admin:users:agreements:set-as-active',
                kwargs={
                    'pk': test_agreement.pk,
                },
            )
        )
        self.assertEqual(response.status_code, 302)

        updated_agreement = Agreement.objects.get(is_active=True)
        self.assertEqual(updated_agreement, test_agreement)

    def test_is_active_type_separation(self):
        """is_active flag is per type"""
        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_TOS,
                'text': 'Lorem ipsum dolor met sit amet elit',
                'is_active': True,
            },
        )

        self.client.post(
            reverse('misago:admin:users:agreements:new'),
            data={
                'type': Agreement.TYPE_PRIVACY,
                'text': 'Lorem ipsum dolor met sit amet elit',
                'is_active': True,
            },
        )

        active_count = Agreement.objects.filter(is_active=True).count()
        self.assertEqual(active_count, 2)
