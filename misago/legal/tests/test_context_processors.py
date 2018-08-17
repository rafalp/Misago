from django.urls import reverse

from misago.legal.context_processors import legal_links
from misago.legal.models import Agreement
from misago.users.testutils import AuthenticatedUserTestCase


class MockRequest(object):
    def __init__(self, user):
        self.user = user
        self.frontend_context = {}

    def get_host(self):
        return 'testhost.com'


class PrivacyPolicyTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(PrivacyPolicyTests, self).setUp()

        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_context_processor_no_policy(self):
        """context processor has no TOS link"""
        context_dict = legal_links(MockRequest(self.user))
        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': None,
            'PRIVACY_POLICY_URL': None,
            'misago_agreement': None,
        })

    def test_context_processor_misago_policy(self):
        """context processor has TOS link to Misago view"""
        Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            text='Lorem ipsum',
            is_active=True,
        )

        context_dict = legal_links(MockRequest(self.user))

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': None,
            'PRIVACY_POLICY_URL': reverse('misago:privacy-policy'),
            'misago_agreement': {
                'title': 'Privacy policy',
                'link': None,
                'text': '<p>Lorem ipsum</p>',
            },
        })

    def test_context_processor_remote_policy(self):
        """context processor has TOS link to remote url"""
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_PRIVACY,
            link='http://test.com',
            is_active=True,
        )

        context_dict = legal_links(MockRequest(self.user))

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': None,
            'PRIVACY_POLICY_URL': 'http://test.com',
            'misago_agreement': {
                'title': 'Privacy policy',
                'link': 'http://test.com',
                'text': None,
            },
        })

        # set misago view too
        agreement.text = 'Lorem ipsum'
        agreement.save()
        
        context_dict = legal_links(MockRequest(self.user))

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': None,
            'PRIVACY_POLICY_URL': 'http://test.com',
            'misago_agreement': {
                'title': 'Privacy policy',
                'link': 'http://test.com',
                'text': '<p>Lorem ipsum</p>',
            },
        })


class TermsOfServiceTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(TermsOfServiceTests, self).setUp()
        
        Agreement.objects.invalidate_cache()

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_context_processor_no_tos(self):
        """context processor has no TOS link"""
        context_dict = legal_links(MockRequest(self.user))
        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': None,
            'PRIVACY_POLICY_URL': None,
            'misago_agreement': None,
        })

    def test_context_processor_misago_tos(self):
        """context processor has TOS link to Misago view"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            text='Lorem ipsum',
            is_active=True,
        )

        context_dict = legal_links(MockRequest(self.user))

        self.assertEqual(
            context_dict, {
                'TERMS_OF_SERVICE_URL': reverse('misago:terms-of-service'),
                'PRIVACY_POLICY_URL': None,
                'misago_agreement': {
                    'title': 'Terms of service',
                    'link': None,
                    'text': '<p>Lorem ipsum</p>',
                }
            }
        )

    def test_context_processor_remote_tos(self):
        """context processor has TOS link to remote url"""
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS,
            link='http://test.com',
            is_active=True,
        )

        context_dict = legal_links(MockRequest(self.user))

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': 'http://test.com',
            'PRIVACY_POLICY_URL': None,
            'misago_agreement': {
                'title': 'Terms of service',
                'link': 'http://test.com',
                'text': None,
            }
        })

        # set misago view too
        agreement.text = 'Lorem ipsum'
        agreement.save()

        context_dict = legal_links(MockRequest(self.user))

        self.assertEqual(context_dict, {
            'TERMS_OF_SERVICE_URL': 'http://test.com',
            'PRIVACY_POLICY_URL': None,
            'misago_agreement': {
                'title': 'Terms of service',
                'link': 'http://test.com',
                'text': '<p>Lorem ipsum</p>',
            },
        })
