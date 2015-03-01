from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.tokens import make_password_change_token


class ForgottenPasswordViewsTests(TestCase):
    def test_request_view_returns_200(self):
        """request new password view returns 200"""
        response = self.client.get(reverse('misago:forgotten_password'))
        self.assertEqual(response.status_code, 200)

    def test_change_view_returns_200(self):
        """change password view returns 200"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.get(
            reverse('misago:forgotten_password_change_form', kwargs={
                'user_id': test_user.id,
                'token': make_password_change_token(test_user)
            }))
        self.assertEqual(response.status_code, 200)

        # test invalid user
        response = self.client.get(
            reverse('misago:forgotten_password_change_form', kwargs={
                'user_id': 7681,
                'token': 'a7d8sa97d98sa798dsa'
            }))
        self.assertEqual(response.status_code, 200)

        # test invalid token
        response = self.client.get(
            reverse('misago:forgotten_password_change_form', kwargs={
                'user_id': test_user.id,
                'token': 'asd79as87ds9a8d7sa'
            }))
        self.assertEqual(response.status_code, 200)
