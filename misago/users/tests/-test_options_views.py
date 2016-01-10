from django.core.urlresolvers import reverse
from misago.users.testutils import AuthenticatedUserTestCase


class OptionsViewsTests(AuthenticatedUserTestCase):
    def test_lander_view_returns_200(self):
        """/options has no show stoppers"""
        response = self.client.get(reverse('misago:options'))
        self.assertEqual(response.status_code, 302)

    def test_form_view_returns_200(self):
        """/options/some-form has no show stoppers"""
        response = self.client.get(reverse('misago:options_form', kwargs={
            'form_name': 'some-fake-form'
        }))
        self.assertEqual(response.status_code, 200)

    def test_token_form_view_returns_200(self):
        """/options/some-form has no show stoppers"""
        response = self.client.get(reverse('misago:options_form', kwargs={
            'form_name': 'some-fake-form',
            'token': 's0m3-t0k3n'
        }))
        self.assertEqual(response.status_code, 200)
