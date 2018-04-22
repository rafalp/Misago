from datetime import timedelta

from django.utils import timezone
from django.urls import reverse

from misago.acl.testutils import override_acl
from misago.categories import THREADS_ROOT_NAME
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Thread
from misago.threads.threadtypes import trees_map
from misago.users.testutils import AuthenticatedUserTestCase


class ThreadsApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadsApiTestCase, self).setUp()

        threads_tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)

        self.root = Category.objects.get(tree_id=threads_tree_id, level=0)
        self.category = Category.objects.get(slug='first-category')

        self.thread = testutils.post_thread(category=self.category)
        self.api_link = self.thread.get_api_url()

    def override_acl(self, acl=None):
        final_acl = self.user.acl_cache['categories'][self.category.pk]
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
            'can_merge_threads': 0,
            'can_close_threads': 0,
        })

        if acl:
            final_acl.update(acl)

        visible_categories = self.user.acl_cache['visible_categories']
        browseable_categories = self.user.acl_cache['browseable_categories']

        if not final_acl['can_see'] and self.category.pk in visible_categories:
            visible_categories.remove(self.category.pk)
            browseable_categories.remove(self.category.pk)

        if not final_acl['can_browse'] and self.category.pk in browseable_categories:
            browseable_categories.remove(self.category.pk)

        override_acl(
            self.user, {
                'visible_categories': visible_categories,
                'browseable_categories': browseable_categories,
                'categories': {
                    self.category.pk: final_acl,
                },
            }
        )

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
        """api has no showstoppers"""
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
            self.override_acl({'can_see_all_threads': 0})

            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

        self.thread.starter = self.user
        self.thread.save()

        for link in self.tested_links:
            self.override_acl({'can_see_all_threads': 0})

            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

    def test_api_validates_category_see_permission(self):
        """api validates category visiblity"""
        for link in self.tested_links:
            self.override_acl({'can_see': 0})

            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

    def test_api_validates_category_browse_permission(self):
        """api validates category browsability"""
        for link in self.tested_links:
            self.override_acl({'can_browse': 0})

            response = self.client.get(link)
            self.assertEqual(response.status_code, 404)

    def test_api_validates_posts_visibility(self):
        """api validates posts visiblity"""
        self.override_acl({'can_hide_posts': 0})

        hidden_post = testutils.reply_thread(
            self.thread,
            is_hidden=True,
            message="I'am hidden test message!",
        )

        response = self.client.get(self.tested_links[1])
        self.assertNotContains(response, hidden_post.parsed)  # post's body is hidden

        # add permission to see hidden posts
        self.override_acl({'can_hide_posts': 1})

        response = self.client.get(self.tested_links[1])
        self.assertContains(
            response, hidden_post.parsed
        )  # hidden post's body is visible with permission

        # unapproved posts shouldn't show at all
        unapproved_post = testutils.reply_thread(
            self.thread,
            is_unapproved=True,
        )

        self.override_acl({'can_approve_content': 0})
        response = self.client.get(self.tested_links[1])
        self.assertNotContains(response, unapproved_post.get_absolute_url())

        # add permission to see unapproved posts
        self.override_acl({'can_approve_content': 1})
        response = self.client.get(self.tested_links[1])
        self.assertContains(response, unapproved_post.parsed)

    def test_api_validates_has_unapproved_posts_visibility(self):
        """api checks acl before exposing unapproved flag"""
        self.thread.has_unapproved_posts = True
        self.thread.save()

        for link in self.tested_links:
            self.override_acl()

            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertEqual(response_json['id'], self.thread.pk)
            self.assertEqual(response_json['title'], self.thread.title)
            self.assertFalse(response_json['has_unapproved_posts'])

        for link in self.tested_links:
            self.override_acl({'can_approve_content': 1})

            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

            response_json = response.json()
            self.assertEqual(response_json['id'], self.thread.pk)
            self.assertEqual(response_json['title'], self.thread.title)
            self.assertTrue(response_json['has_unapproved_posts'])


class ThreadDeleteApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadDeleteApiTests, self).setUp()

        self.last_thread = testutils.post_thread(category=self.category)
        self.api_link = self.last_thread.get_api_url()

    def test_delete_thread_no_permission(self):
        """api tests permission to delete threads"""
        self.override_acl({'can_hide_threads': 0})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.json()['detail'], "You can't delete threads in this category."
        )

        self.override_acl({'can_hide_threads': 1})

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.json()['detail'], "You can't delete threads in this category."
        )

    def test_delete_other_user_thread_no_permission(self):
        """api tests thread owner when deleting own thread"""
        self.override_acl({
            'can_hide_threads': 1,
            'can_hide_own_threads': 2,
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.json()['detail'], "You can't delete other users theads in this category."
        )

    def test_delete_thread_closed_category_no_permission(self):
        """api tests category's closed state"""
        self.category.is_closed = True
        self.category.save()

        self.override_acl({
            'can_hide_threads': 2,
            'can_hide_own_threads': 2,
            'can_close_threads': False,
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.json()['detail'], "This category is closed. You can't delete threads in it."
        )

    def test_delete_thread_closed_no_permission(self):
        """api tests thread's closed state"""
        self.last_thread.is_closed = True
        self.last_thread.save()

        self.override_acl({
            'can_hide_threads': 2,
            'can_hide_own_threads': 2,
            'can_close_threads': False,
        })

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            response.json()['detail'], "This thread is closed. You can't delete it."
        )

    def test_delete_owned_thread_no_time(self):
        """api tests permission to delete owned thread within time limit"""
        self.override_acl({
            'can_hide_threads': 1,
            'can_hide_own_threads': 2,
            'thread_edit_time': 1
        })

        self.last_thread.starter = self.user
        self.last_thread.started_on = timezone.now() - timedelta(minutes=10)
        self.last_thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()['detail'], "You can't delete threads that are older than 1 minute."
        )

    def test_delete_thread(self):
        """DELETE to API link with permission deletes thread"""
        self.override_acl({'can_hide_threads': 2})

        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.last_thread_id, self.last_thread.pk)

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.last_thread.pk)

        # category was synchronised after deletion
        category = Category.objects.get(slug='first-category')
        self.assertEqual(category.last_thread_id, self.thread.pk)

        # test that last thread's deletion triggers category sync
        self.override_acl({'can_hide_threads': 2})

        response = self.client.delete(self.thread.get_api_url())
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        category = Category.objects.get(slug='first-category')
        self.assertIsNone(category.last_thread_id)

    def test_delete_owned_thread(self):
        """api lets owner to delete owned thread within time limit"""
        self.override_acl({
            'can_hide_threads': 1,
            'can_hide_own_threads': 2,
            'thread_edit_time': 30
        })

        self.last_thread.starter = self.user
        self.last_thread.started_on = timezone.now() - timedelta(minutes=10)
        self.last_thread.save()

        response = self.client.delete(self.api_link)
        self.assertEqual(response.status_code, 200)
