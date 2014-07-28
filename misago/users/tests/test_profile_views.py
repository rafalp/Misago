from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase


class UserProfileViewsTests(AdminTestCase):
    def setUp(self):
        super(ChangeForumOptionsTests, self).setUp()
        self.link_kwargs = {
            'user_slug': self.test_admin.slug,
            'user_id': self.test_admin.pk
        }

    def test_user_posts_list(self):
        """user profile posts list has no showstoppers"""
        response = self.client.get(reverse('misago:user_posts'),
                                   kwargs=self.link_kwargs)

        self.assertEqual(response.status_code, 200)
        self.assertIn('posted no messages', response.content)

    def test_user_threads_list(self):
        """user profile threads list has no showstoppers"""
        response = self.client.get(reverse('misago:user_threads'),
                                   kwargs=self.link_kwargs)

        self.assertEqual(response.status_code, 200)
        self.assertIn('started no threads', response.content)
