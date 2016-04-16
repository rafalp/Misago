import json

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase
from misago.categories.models import Category

from misago.threads import testutils
from misago.threads.models import Thread


class ThreadApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')

        self.thread = testutils.post_thread(category=self.category)
        self.api_link = self.thread.get_api_url()

    def override_acl(self, acl):
        final_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_review_moderated_content': 0,
        }
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


class ThreadDeleteApiTests(ThreadApiTestCase):
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


class ThreadsReadApiTests(ThreadApiTestCase):
    def setUp(self):
        super(ThreadSubscribeApiTests, self).setUp()
        self.api_link = '/api/threads/read/'

    def read_all_threads(self):
        """api sets all threads as read"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.categoryread_set.count(), 2)

    def read_threads_in_category(self):
        """api sets threads in category as read"""
        response = self.client.post(
            '%s?category=%s' % (self.api_link, self.category.pk))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.categoryread_set.count(), 1)
