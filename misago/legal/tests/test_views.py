from django.test import TestCase
from django.urls import reverse

from misago.legal.context_processors import legal_links
from misago.legal.models import Agreement


class MockRequest(object):
    def __init__(self):
        self.frontend_context = {}


class PrivacyPolicyTests(TestCase):
    def setUp(self):
        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_404_on_no_policy(self):
        """policy view returns 404 when no policy is set"""
        response = self.client.get(reverse('misago:privacy-policy'))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_policy(self):
        """policy view returns 302 redirect when link is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='http://test.com',
            text='Lorem ipsum',
            is_active=True,
        )

        response = self.client.get(reverse('misago:privacy-policy'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://test.com')

    def test_200_on_link_policy(self):
        """policy view returns 200 when custom tos content is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            title='Test Policy',
            text='Lorem ipsum dolor',
            is_active=True,
        )

        response = self.client.get(reverse('misago:privacy-policy'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Policy')
        self.assertContains(response, 'Lorem ipsum dolor')

    def test_context_processor_no_policy(self):
        """context processor has no TOS link"""
        context_dict = legal_links(MockRequest())
        self.assertFalse(context_dict)

    def test_context_processor_misago_policy(self):
        """context processor has TOS link to Misago view"""
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            text='Lorem ipsum',
            is_active=True,
        )

        context_dict = legal_links(MockRequest())

        self.assertEqual(context_dict, {
            'PRIVACY_POLICY_URL': reverse('misago:privacy-policy'),
        })

    def test_context_processor_remote_policy(self):
        """context processor has TOS link to remote url"""
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='http://test.com',
            is_active=True,
        )

        context_dict = legal_links(MockRequest())

        self.assertEqual(context_dict, {
            'PRIVACY_POLICY_URL': 'http://test.com',
        })

        # set misago view too
        agreement.text = 'Lorem ipsum'
        agreement.save()
        
        context_dict = legal_links(MockRequest())

        self.assertEqual(context_dict, {
            'PRIVACY_POLICY_URL': 'http://test.com',
        })


class TermsOfServiceTests(TestCase):
    def setUp(self):
        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_404_on_no_tos(self):
        """TOS view returns 404 when no TOS is set"""
        response = self.client.get(reverse('misago:terms-of-service'))
        self.assertEqual(response.status_code, 404)

    def test_301_on_link_tos(self):
        """TOS view returns 302 redirect when link is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link='http://test.com',
            text='Lorem ipsum',
            is_active=True,
        )

        response = self.client.get(reverse('misago:terms-of-service'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://test.com')

    def test_200_on_link_tos(self):
        """TOS view returns 200 when custom tos content is set"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            title='Test ToS',
            text='Lorem ipsum dolor',
            is_active=True,
        )

        response = self.client.get(reverse('misago:terms-of-service'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test ToS')
        self.assertContains(response, 'Lorem ipsum dolor')

    def test_context_processor_no_tos(self):
        """context processor has no TOS link"""
        context_dict = legal_links(MockRequest())
        self.assertFalse(context_dict)

    def test_context_processor_misago_tos(self):
        """context processor has TOS link to Misago view"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            text='Lorem ipsum',
            is_active=True,
        )

        context_dict = legal_links(MockRequest())

        self.assertEqual(
            context_dict, {
                'TERMS_OF_SERVICE_URL': reverse('misago:terms-of-service'),
            }
        )

    def test_context_processor_remote_tos(self):
        """context processor has TOS link to remote url"""
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link='http://test.com',
            is_active=True,
        )

        context_dict = legal_links(MockRequest())

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': 'http://test.com',
        })

        # set misago view too
        agreement.text = 'Lorem ipsum'
        agreement.save()

        context_dict = legal_links(MockRequest())

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': 'http://test.com',
        })
