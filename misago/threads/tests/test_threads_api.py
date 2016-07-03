import json

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase
from misago.categories.models import CATEGORIES_TREE_ID, Category

from misago.threads import testutils
from misago.threads.models import Thread


class ThreadsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsApiTestCase, self).setUp()

        self.root = Category.objects.get(tree_id=CATEGORIES_TREE_ID, level=0)
        self.category = Category.objects.get(slug='first-category')

        self.thread = testutils.post_thread(category=self.category)
        self.api_link = self.thread.get_api_url()

    def override_acl(self, acl=None):
        final_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
            'can_edit_posts': 0,
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
        }

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

        return json.loads(response.content)


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

            response_json = json.loads(response.content)
            self.assertEqual(response_json['id'], self.thread.pk)
            self.assertEqual(response_json['title'], self.thread.title)

            if 'posts' in link:
                self.assertIn('post_set', response_json)

    def test_api_shows_owner_thread(self):
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


class ThreadDeleteApiTests(ThreadsApiTestCase):
    def test_delete_thread(self):
        """DELETE to API link with permission deletes thread"""
        self.override_acl({
            'can_hide_threads': 2
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

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

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'],
            "You don't have permission to delete this thread.")

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)


class ThreadsReadApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadsReadApiTests, self).setUp()
        self.api_link = '/api/threads/read/'

    def test_read_all_threads(self):
        """api sets all threads as read"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.categoryread_set.count(), 2)

    def test_read_threads_in_category(self):
        """api sets threads in category as read"""
        response = self.client.post(
            '%s?category=%s' % (self.api_link, self.category.pk))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.categoryread_set.count(), 1)
