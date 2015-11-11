from django.test import TestCase
from misago.core.page import Page


class SiteTests(TestCase):
    def setUp(self):
        self.page = Page('test')

    def test_pages(self):
        """add_section adds section to page"""
        self.page.add_section(
            link='misago:user_posts',
            name='Posts',
            after='misago:user_threads')

        self.page.add_section(
            link='misago:user_threads',
            name='Threads')

        self.page.add_section(
            link='misago:user_follows',
            name='Follows',
            before='misago:user_posts')

        self.page.assert_is_finalized()

        sorted_sections = self.page._sorted_list
        self.assertEqual(sorted_sections[0]['name'], 'Threads')
        self.assertEqual(sorted_sections[1]['name'], 'Follows')
        self.assertEqual(sorted_sections[2]['name'], 'Posts')

        self.assertEqual(self.page.get_default_link(), 'misago:user_threads')
