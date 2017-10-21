from django.test import TestCase
from django.urls import reverse

from misago.conf import settings

from .context_processors import legal_links


class MockRequest(object):
    def __init__(self):
        self.frontend_context = {'url': {}}


class PrivacyPolicyTests(TestCase):
    def tearDown(self):
        settings.reset_settings()

    def test_404_on_no_policy(self):
        """policy view returns 404 when no policy is set"""
        self.assertFalse(settings.privacy_policy_link)
        self.assertFalse(settings.privacy_policy)

        response = self.client.get(reverse('misago:privacy-policy'))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_policy(self):
        """policy view returns 302 redirect when link is set"""
        settings.override_setting('privacy_policy_link', 'http://test.com')
        settings.override_setting('privacy_policy', 'Lorem ipsum')
        self.assertTrue(settings.privacy_policy_link)
        self.assertTrue(settings.privacy_policy)

        response = self.client.get(reverse('misago:privacy-policy'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://test.com')

    def test_200_on_link_policy(self):
        """policy view returns 200 when custom tos content is set"""
        settings.override_setting('privacy_policy_title', 'Test Policy')
        settings.override_setting('privacy_policy', 'Lorem ipsum dolor')
        self.assertTrue(settings.privacy_policy_title)
        self.assertTrue(settings.privacy_policy)

        response = self.client.get(reverse('misago:privacy-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Policy')
        self.assertContains(response, 'Lorem ipsum dolor')

    def test_context_processor_no_policy(self):
        """context processor has no privacy policy link"""
        request = MockRequest()

        context_dict = legal_links(request)
        self.assertFalse(context_dict)
        self.assertEqual(request.frontend_context['url'], {})

    def test_context_processor_misago_policy(self):
        """context processor has TOS link to Misago view"""
        request = MockRequest()

        settings.override_setting('privacy_policy', 'Lorem ipsum')
        legal_links(request)

        self.assertEqual(request.frontend_context['url'], {
            'privacy_policy': reverse('misago:privacy-policy'),
        })

    def test_context_processor_remote_policy(self):
        """context processor has TOS link to remote url"""
        request = MockRequest()

        settings.override_setting('privacy_policy_link', 'http://test.com')
        legal_links(request)

        self.assertEqual(request.frontend_context['url'], {
            'privacy_policy': 'http://test.com',
        })

        # set misago view too
        settings.override_setting('privacy_policy', 'Lorem ipsum')
        legal_links(request)

        self.assertEqual(request.frontend_context['url'], {
            'privacy_policy': 'http://test.com',
        })


class TermsOfServiceTests(TestCase):
    def tearDown(self):
        settings.reset_settings()

    def test_404_on_no_tos(self):
        """TOS view returns 404 when no TOS is set"""
        self.assertFalse(settings.terms_of_service_link)
        self.assertFalse(settings.terms_of_service)

        response = self.client.get(reverse('misago:terms-of-service'))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_tos(self):
        """TOS view returns 302 redirect when link is set"""
        settings.override_setting('terms_of_service_link', 'http://test.com')
        settings.override_setting('terms_of_service', 'Lorem ipsum')
        self.assertTrue(settings.terms_of_service_link)
        self.assertTrue(settings.terms_of_service)

        response = self.client.get(reverse('misago:terms-of-service'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://test.com')

    def test_200_on_link_tos(self):
        """TOS view returns 200 when custom tos content is set"""
        settings.override_setting('terms_of_service_title', 'Test ToS')
        settings.override_setting('terms_of_service', 'Lorem ipsum dolor')
        self.assertTrue(settings.terms_of_service_title)
        self.assertTrue(settings.terms_of_service)

        response = self.client.get(reverse('misago:terms-of-service'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test ToS')
        self.assertContains(response, 'Lorem ipsum dolor')

    def test_context_processor_no_tos(self):
        """context processor has no TOS link"""
        request = MockRequest()

        context_dict = legal_links(request)
        self.assertFalse(context_dict)
        self.assertEqual(request.frontend_context['url'], {})

    def test_context_processor_misago_tos(self):
        """context processor has TOS link to Misago view"""
        request = MockRequest()

        settings.override_setting('terms_of_service', 'Lorem ipsum')
        legal_links(request)

        self.assertEqual(
            request.frontend_context['url'], {
                'tos': reverse('misago:terms-of-service'),
            }
        )

    def test_context_processor_remote_tos(self):
        """context processor has TOS link to remote url"""
        request = MockRequest()

        settings.override_setting('terms_of_service_link', 'http://test.com')
        legal_links(request)

        self.assertEqual(request.frontend_context['url'], {
            'tos': 'http://test.com',
        })

        # set misago view too
        settings.override_setting('terms_of_service', 'Lorem ipsum')
        legal_links(request)

        self.assertEqual(request.frontend_context['url'], {
            'tos': 'http://test.com',
        })
