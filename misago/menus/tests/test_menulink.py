from django.test import TestCase

from ...users.test import create_test_superuser

from ..models import MenuLink


class MenuLinkCreateTest(TestCase):

    def setUp(self):
        MenuLink.objects.create(
            link='https://top_menu_link.com',
            title='Top Menu Link',
            position=MenuLink.POSITION_TOP,
            relevance=600
        )

    def test_menu_link_created_by(self):
        user = create_test_superuser('created_by', 'created_by@misago.com', 'password')

        link = MenuLink.objects.get(
            link='https://top_menu_link.com',
            title='Top Menu Link',
            position=MenuLink.POSITION_TOP,
        )
        self.assertIsNotNone(link)
        self.assertEqual(link.link, 'https://top_menu_link.com')
        self.assertEqual(link.position, MenuLink.POSITION_TOP)

        link.set_created_by(user)

        self.assertEqual(link.created_by, user)
        self.assertEqual(link.created_by_name, user.username)

    def test_menu_link_last_modified_by(self):
        link = MenuLink.objects.get(
            link='https://top_menu_link.com',
            title='Top Menu Link',
            position=MenuLink.POSITION_TOP,
        )
        self.assertIsNotNone(link)

        user = create_test_superuser('misagotestuser', 'test@misago.com', 'testuser')

        link.set_last_modified_by(user)

        self.assertEqual(link.last_modified_by, user)
        self.assertEqual(link.last_modified_by_name, user.username)

