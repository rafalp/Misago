from django.contrib.auth import get_user_model
from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class SearchApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(SearchApiTests, self).setUp()

        self.api_link = reverse('misago:api:search')

    def test_no_permission(self):
        """api respects permission to search users"""
        override_acl(self.user, {'can_search_users': 0})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('users', [p['id'] for p in response.json()])

    def test_no_query(self):
        """api handles no search query"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                self.assertEqual(provider['results']['results'], [])

    def test_empty_query(self):
        """api handles empty search query"""
        response = self.client.get('%s?q=' % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                self.assertEqual(provider['results']['results'], [])

    def test_short_query(self):
        """api handles short search query"""
        response = self.client.get('%s?q=%s' % (self.api_link, self.user.username[0]))
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                results = provider['results']['results']
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]['id'], self.user.id)

    def test_exact_match(self):
        """api handles exact search query"""
        response = self.client.get('%s?q=%s' % (self.api_link, self.user.username))
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                results = provider['results']['results']
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]['id'], self.user.id)

    def test_tail_match(self):
        """api handles last three chars match query"""
        response = self.client.get('%s?q=%s' % (self.api_link, self.user.username[-3:]))
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                results = provider['results']['results']
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]['id'], self.user.id)

    def test_no_match(self):
        """api handles no match"""
        response = self.client.get('%s?q=BobBoberson' % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                self.assertEqual(provider['results']['results'], [])

    def test_search_disabled(self):
        """api respects disabled users visibility"""
        disabled_user = UserModel.objects.create_user(
            'DisabledUser',
            'visible@te.com',
            'Pass.123',
            is_active=False,
        )

        response = self.client.get('%s?q=DisabledUser' % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                self.assertEqual(provider['results']['results'], [])

        # user shows in searchech performed by staff
        self.user.is_staff = True
        self.user.save()

        response = self.client.get('%s?q=DisabledUser' % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn('users', [p['id'] for p in reponse_json])

        for provider in reponse_json:
            if provider['id'] == 'users':
                results = provider['results']['results']
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]['id'], disabled_user.id)


class SearchProviderApiTests(SearchApiTests):
    def setUp(self):
        super(SearchProviderApiTests, self).setUp()

        self.api_link = reverse(
            'misago:api:search', kwargs={
                'search_provider': 'users',
            }
        )
