import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.conf import settings


class TermsOfServiceTests(TestCase):
    def tearDown(self):
        settings.reset_settings()

    def test_404_on_no_tos(self):
        """TOS view returns 404 when no TOS is set"""
        self.assertFalse(settings.terms_of_service_link)
        self.assertFalse(settings.terms_of_service)

        response = self.client.get(reverse('misago:terms_of_service'))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_tos(self):
        """TOS view returns 302 redirect when link is set"""
        settings.override_setting('terms_of_service_link', 'http://test.com')
        settings.override_setting('terms_of_service', 'Lorem ipsum')
        self.assertTrue(settings.terms_of_service_link)
        self.assertTrue(settings.terms_of_service)

        response = self.client.get(reverse('misago:terms_of_service'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://test.com')

    def test_200_on_link_tos(self):
        """TOS view returns 200 when custom tos content is set"""
        settings.override_setting('terms_of_service_title', 'Test ToS')
        settings.override_setting('terms_of_service', 'Lorem ipsum dolor')
        self.assertTrue(settings.terms_of_service_title)
        self.assertTrue(settings.terms_of_service)

        response = self.client.get(reverse('misago:terms_of_service'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test ToS', response.content)
        self.assertIn('Lorem ipsum dolor', response.content)


class PrivacyPolicyTests(TestCase):
    def tearDown(self):
        settings.reset_settings()

    def test_404_on_no_policy(self):
        """policy view returns 404 when no policy is set"""
        self.assertFalse(settings.privacy_policy_link)
        self.assertFalse(settings.privacy_policy)

        response = self.client.get(reverse('misago:privacy_policy'))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_policy(self):
        """policy view returns 302 redirect when link is set"""
        settings.override_setting('privacy_policy_link', 'http://test.com')
        settings.override_setting('privacy_policy', 'Lorem ipsum')
        self.assertTrue(settings.privacy_policy_link)
        self.assertTrue(settings.privacy_policy)

        response = self.client.get(reverse('misago:privacy_policy'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://test.com')

    def test_200_on_link_policy(self):
        """policy view returns 200 when custom tos content is set"""
        settings.override_setting('privacy_policy_title', 'Test Policy')
        settings.override_setting('privacy_policy', 'Lorem ipsum dolor')
        self.assertTrue(settings.privacy_policy_title)
        self.assertTrue(settings.privacy_policy)

        response = self.client.get(reverse('misago:privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Policy', response.content)
        self.assertIn('Lorem ipsum dolor', response.content)


class APIViewTests(TestCase):
    def tearDown(self):
        settings.reset_settings()

    def test_404_responses(self):
        """/legal-pages/ api returns 404 for unset pages"""
        settings.override_setting('privacy_policy_link', '')
        settings.override_setting('privacy_policy', '')
        settings.override_setting('terms_of_service_link', '')
        settings.override_setting('terms_of_service', '')

        response = self.client.get(reverse('misago:api:legal_page', kwargs={
            'page': 'privacy-policy'
        }))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('misago:api:legal_page', kwargs={
            'page': 'terms-of-service'
        }))
        self.assertEqual(response.status_code, 404)

    def test_invalid_page_404_response(self):
        """non-exisisting legal page returns 404"""
        response = self.client.get(
            reverse('misago:api:legal_page', kwargs={'page': 'lol-nope'}))
        self.assertEqual(response.status_code, 404)

    def test_privacy_policy_responses(self):
        """/legal-pages/privacy-policy/ returns valid json"""
        settings.override_setting(
            'privacy_policy_link', 'http://somewhere.com')
        settings.override_setting('privacy_policy', 'I am Bob Boberson!')

        response = self.client.get(reverse('misago:api:legal_page', kwargs={
            'page': 'privacy-policy'
        }))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['id'], 'privacy-policy')
        self.assertEqual(data['link'], 'http://somewhere.com')
        self.assertEqual(data['body'], '<p>I am Bob Boberson!</p>')

    def test_terms_of_service_responses(self):
        """/legal-pages/terms-of-policy/ returns valid json"""
        settings.override_setting(
            'terms_of_service_link', 'http://somewhere.com')
        settings.override_setting('terms_of_service', 'I am Bob Boberson!')

        response = self.client.get(reverse('misago:api:legal_page', kwargs={
            'page': 'terms-of-service'
        }))
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['id'], 'terms-of-service')
        self.assertEqual(data['link'], 'http://somewhere.com')
        self.assertEqual(data['body'], '<p>I am Bob Boberson!</p>')
