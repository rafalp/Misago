from django.test import TestCase
from django.urls import reverse

from ..models import MenuLink


class MenuLinkInFrontendTests(TestCase):

    def setUp(self):
        MenuLink.objects.invalidate_cache()

    def tearDown(self):
        MenuLink.objects.invalidate_cache()

    def test_top_menu_link(self):
        MenuLink.objects.create(
            link='https://test_top_menu_link.com',
            title='Test Top Menu Link',
            position=MenuLink.POSITION_TOP
        )
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://test_top_menu_link.com')
        self.assertContains(response, "Test Top Menu Link")

    def test_footer_menu_link(self):
        MenuLink.objects.create(
            link='https://test_footer_menu_link.com',
            title='Test Footer Menu Link',
            position=MenuLink.POSITION_TOP
        )
        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'https://test_footer_menu_link.com')
        self.assertContains(response, "Test Footer Menu Link")
