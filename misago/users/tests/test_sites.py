from django.test import TestCase
from misago.users.sites import Site


class SiteTests(TestCase):
    def setUp(self):
        self.site = Site('test')

    def test_sites(self):
        """add_page adds page to site"""
        self.site.add_page(link='misago:user_posts',
                           name='Posts',
                           after='misago:user_threads')
        self.site.add_page(link='misago:user_threads',
                           name='Threads')
        self.site.add_page(link='misago:user_follows',
                           name='Follows',
                           before='misago:user_posts')

        self.site.assert_site_is_finalized()
        sorted_pages = self.site._sorted_list
        self.assertEqual(sorted_pages[0]['name'], 'Threads')
        self.assertEqual(sorted_pages[1]['name'], 'Follows')
        self.assertEqual(sorted_pages[2]['name'], 'Posts')

        self.assertEqual(self.site.get_default_link(), 'misago:user_threads')
