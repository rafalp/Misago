from django.test import TestCase, override_settings
from django.urls import reverse

from misago.users.social.utils import get_enabled_social_auth_sites_list


class SocialUtilsTests(TestCase):
    @override_settings(AUTHENTICATION_BACKENDS=[
        'misago.users.authbackends.MisagoBackend',
        'social_core.backends.facebook.FacebookOAuth2',
        'social_core.backends.github.GithubOAuth2',
    ])
    def test_get_enabled_social_auth_sites_list(self):
        self.assertEqual(get_enabled_social_auth_sites_list(), [
            {
                'id': 'facebook',
                'name': 'Facebook',
                'url': reverse('social:begin', kwargs={'backend': 'facebook'}),
            },
            {
                'id': 'github',
                'name': 'GitHub',
                'url': reverse('social:begin', kwargs={'backend': 'github'}),
            }
        ])

    @override_settings(
        AUTHENTICATION_BACKENDS=[
            'misago.users.authbackends.MisagoBackend',
            'social_core.backends.facebook.FacebookOAuth2',
            'social_core.backends.github.GithubOAuth2',
        ],
        MISAGO_SOCIAL_AUTH_BACKENDS_NAMES={
            'facebook': "Facebook Connect",
        }
    )
    def test_get_enabled_social_auth_sites_list_override_name(self):
        self.assertEqual(get_enabled_social_auth_sites_list(), [
            {
                'id': 'facebook',
                'name': 'Facebook Connect',
                'url': reverse('social:begin', kwargs={'backend': 'facebook'}),
            },
            {
                'id': 'github',
                'name': 'GitHub',
                'url': reverse('social:begin', kwargs={'backend': 'github'}),
            }
        ])
