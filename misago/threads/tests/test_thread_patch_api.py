import json

from misago.acl.testutils import override_acl
from misago.categories.models import Category

from misago.threads.tests.test_thread_api import ThreadApiTestCase


class ThreadPinGloballyApiTests(ThreadApiTestCase):
    def test_pin_thread(self):
        """api makes it possible to pin globally thread"""
        self.override_acl({
            'can_pin_threads': 2
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 2}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)

    def test_unpin_thread(self):
        """api makes it possible to unpin thread"""
        self.thread.weight = 2
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)

        self.override_acl({
            'can_pin_threads': 2
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 0}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_pin_thread_no_permission(self):
        """api pin thread globally with no permission fails"""
        self.override_acl({
            'can_pin_threads': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 2}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to pin this thread globally.")

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_unpin_thread_no_permission(self):
        """api unpin thread with no permission fails"""
        self.thread.weight = 2
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)

        self.override_acl({
            'can_pin_threads': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 1}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to change this thread's weight.")

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 2)


class ThreadPinLocallyApiTests(ThreadApiTestCase):
    def test_pin_thread(self):
        """api makes it possible to pin locally thread"""
        self.override_acl({
            'can_pin_threads': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 1}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)

    def test_unpin_thread(self):
        """api makes it possible to unpin thread"""
        self.thread.weight = 1
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)

        self.override_acl({
            'can_pin_threads': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 0}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_pin_thread_no_permission(self):
        """api pin thread locally with no permission fails"""
        self.override_acl({
            'can_pin_threads': 0
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 1}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to change this thread's weight.")

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 0)

    def test_unpin_thread_no_permission(self):
        """api unpin thread with no permission fails"""
        self.thread.weight = 1
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)

        self.override_acl({
            'can_pin_threads': 0
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'weight', 'value': 0}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to change this thread's weight.")

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['weight'], 1)


class ThreadMoveApiTests(ThreadApiTestCase):
    def setUp(self):
        super(ThreadMoveApiTests, self).setUp()

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(self.category, position='last-child', save=True)
        self.category_b = Category.objects.get(slug='category-b')

    def override_other_acl(self, acl):
        final_acl = {
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
        }
        final_acl.update(acl)

        categories_acl = self.user.acl['categories']
        categories_acl[self.category_b.pk] = final_acl

        visible_categories = [self.category.pk]
        if final_acl['can_see']:
            visible_categories.append(self.category_b.pk)

        override_acl(self.user, {
            'visible_categories': visible_categories,
            'categories': categories_acl,
        })

    def test_move_thread(self):
        """api moves thread to other category"""
        self.override_acl({
            'can_move_threads': True
        })
        self.override_other_acl({})

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'category', 'value': self.category_b.pk},
            {'op': 'add', 'path': 'top-category', 'value': self.category_b.pk},
            {'op': 'replace', 'path': 'flatten-categories', 'value': None},
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category_b.pk)

    def test_move_thread_no_permission(self):
        """api move thread to other category with no permission fails"""
        self.override_acl({
            'can_move_threads': False
        })
        self.override_other_acl({})

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'category', 'value': self.category_b.pk}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to move this thread.")

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_move_thread_no_category_access(self):
        """api move thread to category with no access fails"""
        self.override_acl({
            'can_move_threads': True
        })
        self.override_other_acl({
            'can_see': False
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'category', 'value': self.category_b.pk}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0], 'NOT FOUND')

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_move_thread_no_category_browse(self):
        """api move thread to category with no browsing access fails"""
        self.override_acl({
            'can_move_threads': True
        })
        self.override_other_acl({
            'can_browse': False
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'category', 'value': self.category_b.pk}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            'You don\'t have permission to browse "Category B" contents.')

        self.override_other_acl({})

        thread_json = self.get_thread_json()
        self.assertEqual(thread_json['category']['id'], self.category.pk)

    def test_thread_flatten_categories(self):
        """api flatten thread categories"""
        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'flatten-categories', 'value': None}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['category'], self.category.pk)

    def test_thread_top_flatten_categories(self):
        """api flatten thread with top category"""
        self.thread.category = self.category_b
        self.thread.save()

        self.override_other_acl({})

        response = self.client.patch(self.api_link, json.dumps([
            {
                'op': 'add',
                'path': 'top-category',
                'value': Category.objects.root_category().pk,
            },
            {'op': 'replace', 'path': 'flatten-categories', 'value': None},
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['top_category'], self.category.pk)
        self.assertEqual(response_json['category'], self.category_b.pk)


class ThreadCloseApiTests(ThreadApiTestCase):
    def test_close_thread(self):
        """api makes it possible to close thread"""
        self.override_acl({
            'can_close_threads': True
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-closed', 'value': True}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])

    def test_open_thread(self):
        """api makes it possible to open thread"""
        self.thread.is_closed = True
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])

        self.override_acl({
            'can_close_threads': True
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-closed', 'value': False}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_closed'])

    def test_close_thread_no_permission(self):
        """api close thread with no permission fails"""
        self.override_acl({
            'can_close_threads': False
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-closed', 'value': True}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to close this thread.")

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_closed'])

    def test_open_thread_no_permission(self):
        """api open thread with no permission fails"""
        self.thread.is_closed = True
        self.thread.save()

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])

        self.override_acl({
            'can_close_threads': False
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-closed', 'value': False}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to open this thread.")

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_closed'])


class ThreadApproveApiTests(ThreadApiTestCase):
    def test_approve_thread(self):
        """api makes it possible to approve thread"""
        self.thread.is_unapproved = True
        self.thread.save()

        self.override_acl({
            'can_approve_content': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-unapproved', 'value': False}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_unapproved'])

    def test_unapprove_thread(self):
        """api returns permission error on approval removal"""
        self.override_acl({
            'can_approve_content': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-unapproved', 'value': True}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "Content approval can't be reversed.")


class ThreadHideApiTests(ThreadApiTestCase):
    def test_hide_thread(self):
        """api makes it possible to hide thread"""
        self.override_acl({
            'can_hide_threads': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-hidden', 'value': True}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.override_acl({
            'can_hide_threads': 1
        })

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_hidden'])

    def test_show_thread(self):
        """api makes it possible to unhide thread"""
        self.thread.is_hidden = True
        self.thread.save()

        self.override_acl({
            'can_hide_threads': 1
        })

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_hidden'])

        self.override_acl({
            'can_hide_threads': 1
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-hidden', 'value': False}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 200)

        self.override_acl({
            'can_hide_threads': 1
        })

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_hidden'])

    def test_hide_thread_no_permission(self):
        """api hide thread with no permission fails"""
        self.override_acl({
            'can_hide_threads': 0
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-hidden', 'value': True}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['detail'][0],
            "You don't have permission to hide this thread.")

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['is_hidden'])

    def test_show_thread_no_permission(self):
        """api unhide thread with no permission fails"""
        self.thread.is_hidden = True
        self.thread.save()

        self.override_acl({
            'can_hide_threads': 1
        })

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['is_hidden'])

        self.override_acl({
            'can_hide_threads': 0
        })

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'is-hidden', 'value': False}
        ]),
        content_type="application/json")
        self.assertEqual(response.status_code, 404)


class ThreadSubscribeApiTests(ThreadApiTestCase):
    def test_subscribe_thread(self):
        """api makes it possible to subscribe thread"""
        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'subscription', 'value': 'notify'}
        ]),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertFalse(thread_json['subscription'])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertFalse(subscription.send_email)

    def test_subscribe_thread_with_email(self):
        """api makes it possible to subscribe thread with emails"""
        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'subscription', 'value': 'email'}
        ]),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertTrue(thread_json['subscription'])

        subscription = self.user.subscription_set.get(thread=self.thread)
        self.assertTrue(subscription.send_email)

    def test_unsubscribe_thread(self):
        """api makes it possible to unsubscribe thread"""
        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'subscription', 'value': 'remove'}
        ]),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

        thread_json = self.get_thread_json()
        self.assertIsNone(thread_json['subscription'])

        self.assertEqual(self.user.subscription_set.count(), 0)

    def test_subscribe_as_guest(self):
        """api makes it impossible to subscribe thread"""
        self.logout_user()

        response = self.client.patch(self.api_link, json.dumps([
            {'op': 'replace', 'path': 'subscription', 'value': 'email'}
        ]),
        content_type="application/json")

        self.assertEqual(response.status_code, 403)

    def test_subscribe_nonexistant_thread(self):
        """api makes it impossible to subscribe nonexistant thread"""
        bad_api_link = self.api_link.replace(
            unicode(self.thread.pk), unicode(self.thread.pk + 9))

        response = self.client.patch(bad_api_link, json.dumps([
            {'op': 'replace', 'path': 'subscription', 'value': 'email'}
        ]),
        content_type="application/json")

        self.assertEqual(response.status_code, 404)
