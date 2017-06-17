from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl.testutils import override_acl

from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class UserDetailsApiTests(AuthenticatedUserTestCase):
    def test_api_has_no_showstoppers(self):
        """api outputs response for freshly created user"""
        response = self.client.get(
            reverse(
                'misago:api:user-details',
                kwargs={
                    'pk': self.user.pk,
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['edit'])

    def test_api_has_no_showstoppers_old_user(self):
        """api outputs response for freshly created user"""
        self.user.profile_fields = {
            'gender': 'f',
            'bio': 'Lorem ipsum dolor met, sit amet elit, si vis pacem bellum.'
        }
        self.user.save()

        response = self.client.get(
            reverse(
                'misago:api:user-details',
                kwargs={
                    'pk': self.user.pk,
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['edit'])

    def test_other_user(self):
        """api handles scenario when its other user looking at profile"""
        test_user = UserModel.objects.create_user('BobBoberson', 'bob@test.com', 'bob123456')

        api_link = reverse(
            'misago:api:user-details',
            kwargs={
                'pk': test_user.pk,
            }
        )

        # moderator has permission to edit details
        override_acl(self.user, {
            'can_moderate_profile_details': True,
        })

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['edit'])

        # non-moderator has no permission to edit details
        override_acl(self.user, {
            'can_moderate_profile_details': False,
        })

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['edit'])

    def test_nonexistant_user(self):
        """api handles nonexistant users"""
        api_link = reverse(
            'misago:api:user-details',
            kwargs={
                'pk': self.user.pk + 123,
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)
