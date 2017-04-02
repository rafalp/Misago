import json
from datetime import timedelta

from django.utils import six, timezone

from misago.acl.testutils import override_acl
from misago.categories.models import Category

from .test_threads_api import ThreadsApiTestCase


class ThreadPatchApiTestCase(ThreadsApiTestCase):
    def patch(self, api_link, ops):
        return self.client.patch(api_link, json.dumps(ops), content_type="application/json")


class ThreadAddAclApiTests(ThreadPatchApiTestCase):
    def test_add_acl_true(self):
        """api adds current thread's acl to response"""
        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': True,
            },
        ])
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertTrue(response_json['acl'])

    def test_add_acl_false(self):
        """if value is false, api won't add acl to the response, but will set empty key"""
        response = self.patch(self.api_link, [
            {
                'op': 'add',
                'path': 'acl',
                'value': False,
            },
        ])
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertIsNone(response_json['acl'])


class ThreadChangeTitleApiTests(ThreadPatchApiTestCase):
    def test_change_thread_title(self):
        """api makes it possible to change thread title"""
        self.override_acl({'can_edit_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'title',
                    'value': "Lorem ipsum change!",
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['title'], "Lorem ipsum change!")

    def test_change_thread_title_no_permission(self):
        """api validates permission to change title"""
        self.override_acl({'can_edit_threads': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'title',
                    'value': "Lorem ipsum change!",
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "You can't edit threads in this category.")

    def test_change_thread_title_after_edit_time(self):
        """api cleans, validates and rejects too short title"""
        self.override_acl({'thread_edit_time': 1, 'can_edit_threads': 1})

        self.thread.starter = self.user
        self.thread.started_on = timezone.now() - timedelta(minutes=10)
        self.thread.save()

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'title',
                    'value': "Lorem ipsum change!",
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't edit threads that are older than 1 minute."
        )

    def test_change_thread_title_invalid(self):
        """api cleans, validates and rejects too short title"""
        self.override_acl({'can_edit_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'title',
                    'value': 12,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0],
            "Thread title should be at least 5 characters long (it has 2)."
        )


class ThreadPinGloballyApiTests(ThreadPatchApiTestCase):
    def test_pin_thread(self):
        """api makes it possible to pin globally thread"""
        self.override_acl({'can_pin_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 2,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)

    def test_unpin_thread(self):
        """api makes it possible to unpin thread"""
        self.thread.weight = 2
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)

        self.override_acl({'can_pin_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 0,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_pin_thread_no_permission(self):
        """api pin thread globally with no permission fails"""
        self.override_acl({'can_pin_threads': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 2,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to pin this thread globally."
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_unpin_thread_no_permission(self):
        """api unpin thread with no permission fails"""
        self.thread.weight = 2
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)

        self.override_acl({'can_pin_threads': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 1,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to change this thread's weight."
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)


class ThreadPinLocallyApiTests(ThreadPatchApiTestCase):
    def test_pin_thread(self):
        """api makes it possible to pin locally thread"""
        self.override_acl({'can_pin_threads': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 1,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)

    def test_unpin_thread(self):
        """api makes it possible to unpin thread"""
        self.thread.weight = 1
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)

        self.override_acl({'can_pin_threads': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 0,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_pin_thread_no_permission(self):
        """api pin thread locally with no permission fails"""
        self.override_acl({'can_pin_threads': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 1,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to change this thread's weight."
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_unpin_thread_no_permission(self):
        """api unpin thread with no permission fails"""
        self.thread.weight = 1
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)

        self.override_acl({'can_pin_threads': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'weight',
                    'value': 0,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to change this thread's weight."
        )

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)


class ThreadMoveApiTests(ThreadPatchApiTestCase):
    def setUp(self):
        super(ThreadMoveApiTests, self).setUp()

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(
            self.category,
            position='last-child',
            save=True,
        )
        self.category_b = Category.objects.get(slug='category-b')

    def override_other_acl(self, acl):
        other_category_acl = self.user.acl_cache['categories'][self.category.pk].copy()
        other_category_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
        })
        other_category_acl.update(acl)

        categories_acl = self.user.acl_cache['categories']
        categories_acl[self.category_b.pk] = other_category_acl

        visible_categories = [self.category.pk]
        if other_category_acl['can_see']:
            visible_categories.append(self.category_b.pk)

        override_acl(
            self.user, {
                'visible_categories': visible_categories,
                'categories': categories_acl,
            }
        )

    def test_move_thread_no_top(self):
        """api moves thread to other category, sets no top category"""
        self.override_acl({'can_move_threads': True})
        self.override_other_acl({'can_start_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'category',
                    'value': self.category_b.pk,
                },
                {
                    'op': 'add',
                    'path': 'top-category',
                    'value': self.category_b.pk,
                },
                {
                    'op': 'replace',
                    'path': 'flatten-categories',
                    'value': None,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category_b.pk)

        reponse_json = response.json()
        self.assertEqual(reponse_json['category'], self.category_b.pk)

    def test_move_thread_with_top(self):
        """api moves thread to other category, sets top"""
        self.override_acl({'can_move_threads': True})
        self.override_other_acl({'can_start_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'category',
                    'value': self.category_b.pk,
                },
                {
                    'op': 'add',
                    'path': 'top-category',
                    'value': Category.objects.root_category().pk,
                },
                {
                    'op': 'replace',
                    'path': 'flatten-categories',
                    'value': None,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category_b.pk)

        reponse_json = response.json()
        self.assertEqual(reponse_json['category'], self.category_b.pk)

    def test_move_thread_no_permission(self):
        """api move thread to other category with no permission fails"""
        self.override_acl({'can_move_threads': False})
        self.override_other_acl({})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'category',
                    'value': self.category_b.pk,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to move this thread."
        )

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_move_thread_no_category_access(self):
        """api move thread to category with no access fails"""
        self.override_acl({'can_move_threads': True})
        self.override_other_acl({'can_see': False})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'category',
                    'value': self.category_b.pk,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], 'NOT FOUND')

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_move_thread_no_category_browse(self):
        """api move thread to category with no browsing access fails"""
        self.override_acl({'can_move_threads': True})
        self.override_other_acl({'can_browse': False})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'category',
                    'value': self.category_b.pk,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0],
            'You don\'t have permission to browse "Category B" contents.'
        )

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_move_thread_same_category(self):
        """api move thread to category it's already in fails"""
        self.override_acl({'can_move_threads': True})
        self.override_other_acl({'can_start_threads': 2})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'category',
                    'value': self.thread.category_id,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You can't move thread to the category it's already in."
        )

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_thread_flatten_categories(self):
        """api flatten thread categories"""
        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'flatten-categories',
                    'value': None,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['category'], self.category.pk)


class ThreadCloseApiTests(ThreadPatchApiTestCase):
    def test_close_thread(self):
        """api makes it possible to close thread"""
        self.override_acl({'can_close_threads': True})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-closed',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])

    def test_open_thread(self):
        """api makes it possible to open thread"""
        self.thread.is_closed = True
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])

        self.override_acl({'can_close_threads': True})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-closed',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_closed'])

    def test_close_thread_no_permission(self):
        """api close thread with no permission fails"""
        self.override_acl({'can_close_threads': False})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-closed',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to close this thread."
        )

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_closed'])

    def test_open_thread_no_permission(self):
        """api open thread with no permission fails"""
        self.thread.is_closed = True
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])

        self.override_acl({'can_close_threads': False})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-closed',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to open this thread."
        )

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])


class ThreadApproveApiTests(ThreadPatchApiTestCase):
    def test_approve_thread(self):
        """api makes it possible to approve thread"""
        self.thread.is_unapproved = True
        self.thread.save()

        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_unapproved'])

    def test_unapprove_thread(self):
        """api returns permission error on approval removal"""
        self.override_acl({'can_approve_content': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-unapproved',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json['detail'][0], "Content approval can't be reversed.")


class ThreadHideApiTests(ThreadPatchApiTestCase):
    def test_hide_thread(self):
        """api makes it possible to hide thread"""
        self.override_acl({'can_hide_threads': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_hide_threads': 1})

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_hidden'])

    def test_show_thread(self):
        """api makes it possible to unhide thread"""
        self.thread.is_hidden = True
        self.thread.save()

        self.override_acl({'can_hide_threads': 1})

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_hidden'])

        self.override_acl({'can_hide_threads': 1})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 200)

        self.override_acl({'can_hide_threads': 1})

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_hidden'])

    def test_hide_thread_no_permission(self):
        """api hide thread with no permission fails"""
        self.override_acl({'can_hide_threads': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': True,
                },
            ]
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['detail'][0], "You don't have permission to hide this thread."
        )

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_hidden'])

    def test_show_thread_no_permission(self):
        """api unhide thread with no permission fails"""
        self.thread.is_hidden = True
        self.thread.save()

        self.override_acl({'can_hide_threads': 1})

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_hidden'])

        self.override_acl({'can_hide_threads': 0})

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'is-hidden',
                    'value': False,
                },
            ]
        )
        self.assertEqual(response.status_code, 404)


class ThreadSubscribeApiTests(ThreadPatchApiTestCase):
    def test_subscribe_thread(self):
        """api makes it possible to subscribe thread"""
        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'subscription',
                    'value': 'notify',
                },
            ]
        )

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['subscription'])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertFalse(subscription.send_email)

    def test_subscribe_thread_with_email(self):
        """api makes it possible to subscribe thread with emails"""
        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'subscription',
                    'value': 'email',
                },
            ]
        )

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['subscription'])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertTrue(subscription.send_email)

    def test_unsubscribe_thread(self):
        """api makes it possible to unsubscribe thread"""
        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'subscription',
                    'value': 'remove',
                },
            ]
        )

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json['subscription'])

        self.assertEqual(self.user.subscription_set.count(), 0)

    def test_subscribe_as_guest(self):
        """api makes it impossible to subscribe thread"""
        self.logout_user()

        response = self.patch(
            self.api_link, [
                {
                    'op': 'replace',
                    'path': 'subscription',
                    'value': 'email',
                },
            ]
        )

        self.assertEqual(response.status_code, 403)

    def test_subscribe_nonexistant_thread(self):
        """api makes it impossible to subscribe nonexistant thread"""
        bad_api_link = self.api_link.replace(
            six.text_type(self.thread.pk), six.text_type(self.thread.pk + 9)
        )

        response = self.patch(
            bad_api_link, [
                {
                    'op': 'replace',
                    'path': 'subscription',
                    'value': 'email',
                },
            ]
        )

        self.assertEqual(response.status_code, 404)
