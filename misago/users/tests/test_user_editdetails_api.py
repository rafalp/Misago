from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl.testutils import override_acl

from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class UserEditDetailsApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(UserEditDetailsApiTests, self).setUp()

        self.api_link = reverse(
            'misago:api:user-edit-details',
            kwargs={
                'pk': self.user.pk,
            }
        )

    def get_profile_fields(self):
        return UserModel.objects.get(pk=self.user.pk).profile_fields

    def test_api_has_no_showstoppers(self):
        """api outputs response for freshly created user"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_api_has_no_showstoppers_old_user(self):
        """api outputs response for freshly created user"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_other_user(self):
        """api handles scenario when its other user looking at profile"""
        test_user = UserModel.objects.create_user('BobBoberson', 'bob@test.com', 'bob123456')

        api_link = reverse(
            'misago:api:user-edit-details',
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

        # non-moderator has no permission to edit details
        override_acl(self.user, {
            'can_moderate_profile_details': False,
        })

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 403)

    def test_nonexistant_user(self):
        """api handles nonexistant users"""
        api_link = reverse(
            'misago:api:user-edit-details',
            kwargs={
                'pk': self.user.pk + 123,
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)

    def test_api_updates_text_field(self):
        """api updates text field"""
        response = self.client.post(self.api_link, data={
            'bio': 'I have some, as is tradition.'
        })
        self.assertEqual(response.status_code, 200)

        profile_fields = self.get_profile_fields()
        self.assertEqual(profile_fields['bio'], 'I have some, as is tradition.')

        response_json = response.json()
        self.assertEqual(response_json['id'], self.user.id)
        self.assertTrue(response_json['edit'])
        self.assertTrue(response_json['groups'])

    def test_api_updates_select_field(self):
        """api updates select field"""
        response = self.client.post(self.api_link, data={
            'gender': 'female',
        })

        self.assertEqual(response.status_code, 200)

        profile_fields = self.get_profile_fields()
        self.assertEqual(profile_fields['gender'], 'female')

        response_json = response.json()
        self.assertEqual(response_json['id'], self.user.id)
        self.assertTrue(response_json['edit'])
        self.assertTrue(response_json['groups'])

    def test_api_validates_url_field(self):
        """api runs basic validation against url fields"""
        response = self.client.post(self.api_link, data={
            'website': 'noturl',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'website': ['Enter a valid URL.']})

    def test_api_cleans_url_field(self):
        """api cleans url fields"""
        response = self.client.post(self.api_link, data={
            'website': 'onet.pl',
        })

        self.assertEqual(response.status_code, 200)

        profile_fields = self.get_profile_fields()
        self.assertEqual(profile_fields['website'], 'http://onet.pl')

        response_json = response.json()
        self.assertEqual(response_json['id'], self.user.id)
        self.assertTrue(response_json['edit'])
        self.assertTrue(response_json['groups'])

    def test_api_custom_cleans_url_field(self):
        """api calls fields clean method"""
        response = self.client.post(self.api_link, data={
            'twitter': '@Weebl',
        })

        self.assertEqual(response.status_code, 200)

        profile_fields = self.get_profile_fields()
        self.assertEqual(profile_fields['twitter'], 'Weebl')

        response_json = response.json()
        self.assertEqual(response_json['id'], self.user.id)
        self.assertTrue(response_json['edit'])
        self.assertTrue(response_json['groups'])
