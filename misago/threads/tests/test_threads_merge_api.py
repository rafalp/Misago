import json

from django.core.urlresolvers import reverse

from misago.acl import add_acl
from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.api.threadendpoints.merge import MERGE_LIMIT
from misago.threads.models import Post, Thread
from misago.threads.serializers import ThreadListSerializer
from misago.threads.tests.test_threads_api import ThreadsApiTestCase


class ThreadsMergeApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadsMergeApiTests, self).setUp()
        self.api_link = reverse('misago:api:thread-merge')

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(self.category, position='last-child', save=True)
        self.category_b = Category.objects.get(slug='category-b')

    def test_merge_no_threads(self):
        """api validates if we are trying to merge no threads"""
        response = self.client.post(self.api_link, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "You have to select at least two threads to merge."
        })

    def test_merge_empty_threads(self):
        """api validates if we are trying to empty threads list"""
        response = self.client.post(self.api_link, json.dumps({
            'threads': []
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "You have to select at least two threads to merge."
        })

    def test_merge_invalid_threads(self):
        """api validates if we are trying to merge invalid thread ids"""
        response = self.client.post(self.api_link, json.dumps({
            'threads': 'abcd'
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "One or more thread ids received were invalid."
        })

        response = self.client.post(self.api_link, json.dumps({
            'threads': ['a', '-', 'c']
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "One or more thread ids received were invalid."
        })

    def test_merge_single_thread(self):
        """api validates if we are trying to merge single thread"""
        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id]
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "You have to select at least two threads to merge."
        })

    def test_merge_with_nonexisting_thread(self):
        """api validates if we are trying to merge with invalid thread"""
        unaccesible_thread = testutils.post_thread(category=self.category_b)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, self.thread.id + 1000]
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "One or more threads to merge could not be found."
        })

    def test_merge_with_invisible_thread(self):
        """api validates if we are trying to merge with inaccesible thread"""
        unaccesible_thread = testutils.post_thread(category=self.category_b)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, unaccesible_thread.id]
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "One or more threads to merge could not be found."
        })

    def test_merge_no_permission(self):
        """api validates permission to merge threads"""
        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id]
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, [
            {
                'id': thread.pk,
                'title': thread.title,
                'errors': [
                    "You don't have permission to merge this thread with others."
                ]
            },
            {
                'id': self.thread.pk,
                'title': self.thread.title,
                'errors': [
                    "You don't have permission to merge this thread with others."
                ]
            },
        ])

    def test_merge_too_many_threads(self):
        """api rejects too many threads to merge"""
        threads = []
        for i in xrange(MERGE_LIMIT + 1):
            threads.append(testutils.post_thread(category=self.category).pk)

        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        response = self.client.post(self.api_link, json.dumps({
            'threads': threads
        }), content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'detail': "No more than %s threads can be merged at single time." % MERGE_LIMIT
        })

    def test_merge_no_final_thread(self):
        """api rejects merge because no data to merge threads was specified"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id]
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'title': ['This field is required.'],
            'category': ['This field is required.'],
        })

    def test_merge_invalid_final_title(self):
        """api rejects merge because final thread title was invalid"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': '$$$',
            'category': self.category.id,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'title': ["Thread title should be at least 5 characters long."]
        })

    def test_merge_invalid_category(self):
        """api rejects merge because final category was invalid"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': 'Valid thread title',
            'category': self.category_b.id,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'category': ["Requested category could not be found."]
        })

    def test_merge_invalid_weight(self):
        """api rejects merge because final weight was invalid"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': 'Valid thread title',
            'category': self.category.id,
            'weight': 4,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'weight': ["Ensure this value is less than or equal to 2."]
        })

    def test_merge_unallowed_global_weight(self):
        """api rejects merge because global weight was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': 'Valid thread title',
            'category': self.category.id,
            'weight': 2,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'weight': [
                "You don't have permission to pin threads globally in this category."
            ]
        })

    def test_merge_unallowed_local_weight(self):
        """api rejects merge because local weight was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': 'Valid thread title',
            'category': self.category.id,
            'weight': 1,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'weight': [
                "You don't have permission to pin threads in this category."
            ]
        })

    def test_merge_allowed_local_weight(self):
        """api allows local weight"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_pin_threads': 1,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': '$$$',
            'category': self.category.id,
            'weight': 1,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'title': ["Thread title should be at least 5 characters long."]
        })

    def test_merge_allowed_global_weight(self):
        """api allows local weight"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_pin_threads': 2,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': '$$$',
            'category': self.category.id,
            'weight': 2,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'title': ["Thread title should be at least 5 characters long."]
        })

    def test_merge_unallowed_close(self):
        """api rejects merge because closing thread was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': 'Valid thread title',
            'category': self.category.id,
            'is_closed': True,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'is_closed': [
                "You don't have permission to close threads in this category."
            ]
        })

    def test_merge_with_close(self):
        """api allows for closing thread"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_close_threads': True,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': '$$$',
            'category': self.category.id,
            'weight': 0,
            'is_closed': True,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.content)
        self.assertEqual(response_json, {
            'title': ["Thread title should be at least 5 characters long."]
        })

    def test_merge(self):
        """api performs basic merge"""
        posts_ids = [p.id for p in Post.objects.all()]

        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'threads': [self.thread.id, thread.id],
            'title': 'Merged thread!',
            'category': self.category.id,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # is response json with new thread?
        response_json = json.loads(response.content)

        new_thread = Thread.objects.get(pk=response_json['id'])
        new_thread.is_read = False
        new_thread.subscription = None
        new_thread.top_category = None

        add_acl(self.user, new_thread.category)
        add_acl(self.user, new_thread)

        self.assertEqual(response_json, ThreadListSerializer(new_thread).data)

        # did posts move to new thread?
        for post in Post.objects.filter(id__in=posts_ids):
            self.assertEqual(post.thread_id, new_thread.id)

        # are old threads gone?
        self.assertEqual([t.pk for t in Thread.objects.all()], [new_thread.pk])

    def test_merge_with_top_category(self):
        """api performs merge with top category"""
        posts_ids = [p.id for p in Post.objects.all()]

        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(self.api_link, json.dumps({
            'top_category': self.root.id,
            'threads': [self.thread.id, thread.id],
            'title': 'Merged thread!',
            'category': self.category.id,
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # is response json with new thread?
        response_json = json.loads(response.content)

        new_thread = Thread.objects.get(pk=response_json['id'])
        new_thread.is_read = False
        new_thread.subscription = None
        new_thread.top_category = self.category

        add_acl(self.user, new_thread.category)
        add_acl(self.user, new_thread)

        self.assertEqual(response_json, ThreadListSerializer(new_thread).data)

        # did posts move to new thread?
        for post in Post.objects.filter(id__in=posts_ids):
            self.assertEqual(post.thread_id, new_thread.id)

        # are old threads gone?
        self.assertEqual([t.pk for t in Thread.objects.all()], [new_thread.pk])
