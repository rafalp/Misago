from misago.acl.testutils import override_acl
from misago.categories.models import THREADS_ROOT_NAME, Category
from misago.users.testutils import AuthenticatedUserTestCase

from .. import testutils
from ..models import Thread
from ..threadtypes import trees_map


class ThreadsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsApiTestCase, self).setUp()

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

        self.root = Category.objects.get(tree_id=threads_tree_id, level=0)
        self.category = Category.objects.get(slug='first-category')

        self.thread = testutils.post_thread(category=self.category)
        self.api_link = self.thread.get_api_url()

    def override_acl(self, acl=None):
        final_acl = self.user.acl['categories'][self.category.pk]
        final_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
            'can_edit_posts': 0,
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
            'can_merge_threads': 0
        })

        if acl:
            final_acl.update(acl)

        override_acl(self.user, {
            'categories': {
                self.category.pk: final_acl
            }
        })

    def get_thread_json(self):
        response = self.client.get(self.thread.get_api_url())
        self.assertEqual(response.status_code, 200)

        return response.json()


class ThreadRetrieveApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadRetrieveApiTests, self).setUp()

        self.tested_links = [
            self.api_link,
            '%sposts/' % self.api_link,
            '%sposts/?page=1' % self.api_link,
        ]

    def test_api_returns_thread(self):
        """api endpoint has no showstoppers"""
        for link in self.tested_links:
            self.override_acl()

            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertEqual(response_json['id'], self.thread.pk)
            self.assertEqual(response_json['title'], self.thread.title)

            if 'posts' in link:
                self.assertIn('post_set', response_json)

    def test_api_shows_owned_thread(self):
        """api handles "owned threads only"""
        for link in self.tested_links:
            self.override_acl({
                'can_see_all_threads': 0
            })

            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

        self.thread.starter = self.user
        self.thread.save()

        for link in self.tested_links:
            self.override_acl({
                'can_see_all_threads': 0
            })

            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

    def test_api_validates_category_permissions(self):
        """api endpoint validates category visiblity"""
        for link in self.tested_links:
            self.override_acl({
                'can_see': 0
            })

            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

        for link in self.tested_links:
            self.override_acl({
                'can_browse': 0
            })

            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

    def test_api_validates_posts_visibility(self):
        """api endpoint validates posts visiblity"""
        self.override_acl({
            'can_hide_posts': 0
        })

        hidden_post = testutils.reply_thread(self.thread, is_hidden=True, message="I'am hidden test message!")

        response = self.client.get(self.tested_links[1])
        self.assertNotContains(response, hidden_post.parsed) # post's body is hidden

        # add permission to see hidden posts
        self.override_acl({
            'can_hide_posts': 1
        })

        response = self.client.get(self.tested_links[1])
        self.assertContains(response, hidden_post.parsed) # hidden post's body is visible with permission

        self.override_acl({
            'can_approve_content': 0
        })

        # unapproved posts shouldn't show at all
        unapproved_post = testutils.reply_thread(self.thread, is_unapproved=True)

        response = self.client.get(self.tested_links[1])
        self.assertNotContains(response, unapproved_post.get_absolute_url())

        # add permission to see unapproved posts
        self.override_acl({
            'can_approve_content': 1
        })

        response = self.client.get(self.tested_links[1])
        self.assertContains(response, unapproved_post.get_absolute_url())


class ThreadDeleteApiTests(ThreadsApiTestCase):
    def test_delete_thread_no_permission(self):
        """DELETE to API link with no permission to delete fails"""
        self.override_acl({
            'can_hide_threads': 1
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

        self.override_acl({
            'can_hide_threads': 0
        })

        response_json = response.json()
        self.assertEqual(response_json['detail'],
            "You don't have permission to delete this thread.")

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_delete_thread(self):
        """DELETE to API link with permission deletes thread"""
        self.override_acl({
            'can_hide_threads': 2
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)
