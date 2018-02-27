import json

from django.urls import reverse

from misago.acl import add_acl
from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.readtracker import poststracker
from misago.threads import testutils
from misago.threads.serializers.moderation import THREADS_LIMIT
from misago.threads.models import Poll, PollVote, Post, Thread
from misago.threads.serializers import ThreadsListSerializer

from .test_threads_api import ThreadsApiTestCase


class ThreadsMergeApiTests(ThreadsApiTestCase):
    def setUp(self):
        super(ThreadsMergeApiTests, self).setUp()
        self.api_link = reverse('misago:api:thread-merge')

        Category(
            name='Category B',
            slug='category-b',
        ).insert_at(
            self.category,
            position='last-child',
            save=True,
        )
        self.category_b = Category.objects.get(slug='category-b')

    def override_other_category(self):
        categories =  self.user.acl_cache['categories']

        visible_categories = self.user.acl_cache['visible_categories']
        browseable_categories = self.user.acl_cache['browseable_categories']

        visible_categories.append(self.category_b.pk)
        browseable_categories.append(self.category_b.pk)

        override_acl(
            self.user, {
                'visible_categories': visible_categories,
                'browseable_categories': browseable_categories,
                'categories': {
                    self.category.pk: categories[self.category.pk],
                    self.category_b.pk: {
                        'can_see': 1,
                        'can_browse': 1,
                        'can_see_all_threads': 1,
                        'can_see_own_threads': 0,
                        'can_start_threads': 2,
                    },
                },
            }
        )

    def test_merge_no_threads(self):
        """api validates if we are trying to merge no threads"""
        response = self.client.post(self.api_link, content_type="application/json")
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['threads'], ["You have to select at least two threads to merge."]
        )

    def test_merge_empty_threads(self):
        """api validates if we are trying to empty threads list"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['threads'], ["You have to select at least two threads to merge."]
        )

    def test_merge_invalid_threads(self):
        """api validates if we are trying to merge invalid thread ids"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': 'abcd',
            }),
            content_type="application/json",
        )
        self.assertContains(response, "Expected a list of items", status_code=400)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': ['a', '-', 'c'],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['threads'], ["One or more thread ids received were invalid."]
        )

    def test_merge_single_thread(self):
        """api validates if we are trying to merge single thread"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['threads'], ["You have to select at least two threads to merge."]
        )

    def test_merge_with_nonexisting_thread(self):
        """api validates if we are trying to merge with invalid thread"""
        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, self.thread.id + 1000],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['threads'], ["One or more threads to merge could not be found."]
        )

    def test_merge_with_invisible_thread(self):
        """api validates if we are trying to merge with inaccesible thread"""
        unaccesible_thread = testutils.post_thread(category=self.category_b)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, unaccesible_thread.id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json['threads'], ["One or more threads to merge could not be found."]
        )

    def test_merge_no_permission(self):
        """api validates permission to merge threads"""
        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'category': self.category.pk,
                'title': 'Lorem ipsum dolor',
                'threads': [self.thread.id, thread.id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'merge': [
                    {
                        'id': str(thread.pk),
                        'detail': ["You can't merge threads in this category."],
                    },
                    {
                        'id': str(self.thread.pk),
                        'detail': ["You can't merge threads in this category."],
                    },
                ],
            }
        )

    def test_thread_category_is_closed(self):
        """api validates if thread's category is open"""
        self.override_acl({
            'can_merge_threads': 1,
            'can_close_threads': 0,
        })
        self.override_other_category()

        other_thread = testutils.post_thread(self.category)

        self.category.is_closed = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            json.dumps({
                'category': self.category_b.pk,
                'title': 'Lorem ipsum dolor',
                'threads': [self.thread.id, other_thread.id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'merge': [
                    {
                        'id': str(other_thread.pk),
                        'detail': ["This category is closed. You can't merge it's threads."],
                    },
                    {
                        'id': str(self.thread.pk),
                        'detail': ["This category is closed. You can't merge it's threads."],
                    },
                ],
            }
        )

    def test_thread_is_closed(self):
        """api validates if thread is open"""
        self.override_acl({
            'can_merge_threads': 1,
            'can_close_threads': 0,
        })
        self.override_other_category()

        other_thread = testutils.post_thread(self.category)

        other_thread.is_closed = True
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps({
                'category': self.category_b.pk,
                'title': 'Lorem ipsum dolor',
                'threads': [self.thread.id, other_thread.id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'merge': [
                    {
                        'id': str(other_thread.pk),
                        'detail': [
                            "This thread is closed. You can't merge it with other threads."
                        ],
                    },
                ],
            }
        )

    def test_merge_too_many_threads(self):
        """api rejects too many threads to merge"""
        threads = []
        for _ in range(THREADS_LIMIT + 1):
            threads.append(testutils.post_thread(category=self.category).pk)

        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })
        self.override_other_category()

        response = self.client.post(
            self.api_link,
            json.dumps({
                'category': self.category_b.pk,
                'title': 'Lorem ipsum dolor',
                'threads': threads,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'threads': [
                    "No more than %s threads can be merged at single time." % THREADS_LIMIT
                ],
            }
        )

    def test_merge_no_final_thread(self):
        """api rejects merge because no data to merge threads was specified"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ['This field is required.'],
                'category': ['This field is required.'],
            }
        )

    def test_merge_invalid_final_title(self):
        """api rejects merge because final thread title was invalid"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': '$$$',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_merge_invalid_category(self):
        """api rejects merge because final category was invalid"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category_b.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'category': ["Requested category could not be found."],
            }
        )

    def test_merge_unallowed_start_thread(self):
        """api rejects merge because category isn't allowing starting threads"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_start_threads': 0,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'category': ["You can't create new threads in selected category."],
            }
        )

    def test_merge_invalid_weight(self):
        """api rejects merge because final weight was invalid"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category.id,
                'weight': 4,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'weight': ["Ensure this value is less than or equal to 2."],
            }
        )

    def test_merge_unallowed_global_weight(self):
        """api rejects merge because global weight was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category.id,
                'weight': 2,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'weight': ["You don't have permission to pin threads globally in this category."],
            }
        )

    def test_merge_unallowed_local_weight(self):
        """api rejects merge because local weight was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category.id,
                'weight': 1,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'weight': ["You don't have permission to pin threads in this category."],
            }
        )

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

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': '$$$',
                'category': self.category.id,
                'weight': 1,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_merge_allowed_global_weight(self):
        """api allows global weight"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_pin_threads': 2,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': '$$$',
                'category': self.category.id,
                'weight': 2,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_merge_unallowed_close(self):
        """api rejects merge because closing thread was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category.id,
                'is_closed': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'is_closed': ["You don't have permission to close threads in this category."],
            }
        )

    def test_merge_with_close(self):
        """api allows for closing thread"""
        self.override_acl({
            'can_merge_threads': True,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_close_threads': True,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': '$$$',
                'category': self.category.id,
                'weight': 0,
                'is_closed': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

    def test_merge_unallowed_hidden(self):
        """api rejects merge because hidden thread was unallowed"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_hide_threads': 0,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Valid thread title',
                'category': self.category.id,
                'is_hidden': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'is_hidden': ["You don't have permission to hide threads in this category."],
            }
        )

    def test_merge_with_hide(self):
        """api allows for hiding thread"""
        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': False,
            'can_edit_threads': False,
            'can_reply_threads': False,
            'can_hide_threads': 1,
        })

        thread = testutils.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': '$$$',
                'category': self.category.id,
                'weight': 0,
                'is_hidden': True,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {
                'title': ["Thread title should be at least 5 characters long (it has 3)."],
            }
        )

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

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # is response json with new thread?
        response_json = response.json()

        new_thread = Thread.objects.get(pk=response_json['id'])
        new_thread.is_read = False
        new_thread.subscription = None

        add_acl(self.user, new_thread.category)
        add_acl(self.user, new_thread)

        self.assertEqual(response_json, ThreadsListSerializer(new_thread).data)

        # did posts move to new thread?
        for post in Post.objects.filter(id__in=posts_ids):
            self.assertEqual(post.thread_id, new_thread.id)

        # are old threads gone?
        self.assertEqual([t.pk for t in Thread.objects.all()], [new_thread.pk])

    def test_merge_kitchensink(self):
        """api performs merge"""
        posts_ids = [p.id for p in Post.objects.all()]

        self.override_acl({
            'can_merge_threads': True,
            'can_close_threads': True,
            'can_hide_threads': 1,
            'can_pin_threads': 2,
        })

        thread = testutils.post_thread(category=self.category)

        poststracker.save_read(self.user, self.thread.first_post)
        poststracker.save_read(self.user, thread.first_post)

        self.user.subscription_set.create(
            thread=self.thread,
            category=self.thread.category,
            last_read_on=self.thread.last_post_on,
            send_email=False,
        )
        self.user.subscription_set.create(
            thread=thread,
            category=thread.category,
            last_read_on=thread.last_post_on,
            send_email=False,
        )

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
                'is_closed': 1,
                'is_hidden': 1,
                'weight': 2,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # is response json with new thread?
        response_json = response.json()

        new_thread = Thread.objects.get(pk=response_json['id'])
        new_thread.is_read = False
        new_thread.subscription = None

        self.assertEqual(new_thread.weight, 2)
        self.assertTrue(new_thread.is_closed)
        self.assertTrue(new_thread.is_hidden)

        add_acl(self.user, new_thread.category)
        add_acl(self.user, new_thread)

        self.assertEqual(response_json, ThreadsListSerializer(new_thread).data)

        # did posts move to new thread?
        for post in Post.objects.filter(id__in=posts_ids):
            self.assertEqual(post.thread_id, new_thread.id)

        # are old threads gone?
        self.assertEqual([t.pk for t in Thread.objects.all()], [new_thread.pk])

        # posts reads are kept
        postreads = self.user.postread_set.filter(post__is_event=False).order_by('id')

        self.assertEqual(
            list(postreads.values_list('post_id', flat=True)),
            [self.thread.first_post_id, thread.first_post_id]
        )
        self.assertEqual(postreads.filter(thread=new_thread).count(), 2)
        self.assertEqual(postreads.filter(category=self.category).count(), 2)

        # subscriptions are kept
        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=new_thread)
        self.user.subscription_set.get(category=self.category)

    def test_merge_threads_kept_poll(self):
        """api merges two threads successfully, keeping poll from old thread"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)
        poll = testutils.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        new_thread = Thread.objects.get(pk=response_json['id'])

        # poll and its votes were kept
        self.assertEqual(Poll.objects.filter(pk=poll.pk, thread=new_thread).count(), 1)
        self.assertEqual(PollVote.objects.filter(poll=poll, thread=new_thread).count(), 4)

        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

    def test_merge_threads_moved_poll(self):
        """api merges two threads successfully, moving poll from other thread"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)
        poll = testutils.post_poll(self.thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        new_thread = Thread.objects.get(pk=response_json['id'])

        # poll and its votes were kept
        self.assertEqual(Poll.objects.filter(pk=poll.pk, thread=new_thread).count(), 1)
        self.assertEqual(PollVote.objects.filter(poll=poll, thread=new_thread).count(), 4)

        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

    def test_threads_merge_conflict(self):
        """api errors on merge conflict, returning list of available polls"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)
        poll = testutils.post_poll(self.thread, self.user)
        other_poll = testutils.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'polls': [
                    ['0', "Delete all polls"],
                    [str(poll.pk), poll.question],
                    [str(other_poll.pk), other_poll.question],
                ],
            }
        )

        # polls and votes were untouched
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(PollVote.objects.count(), 8)

    def test_threads_merge_conflict_invalid_resolution(self):
        """api errors on invalid merge conflict resolution"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)

        testutils.post_poll(self.thread, self.user)
        testutils.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
                'poll': 'dsa7dsadsa9789',
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'poll': ["Invalid choice."],
        })

        # polls and votes were untouched
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(PollVote.objects.count(), 8)

    def test_threads_merge_conflict_delete_all(self):
        """api deletes all polls when delete all choice is selected"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)

        testutils.post_poll(self.thread, self.user)
        testutils.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
                'poll': 0,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # polls and votes are gone
        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(PollVote.objects.count(), 0)

    def test_threads_merge_conflict_keep_first_poll(self):
        """api deletes other poll on merge"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)
        poll = testutils.post_poll(self.thread, self.user)
        other_poll = testutils.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
                'poll': poll.pk,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # other poll and its votes are gone
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

        Poll.objects.get(pk=poll.pk)
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(pk=other_poll.pk)

    def test_threads_merge_conflict_keep_other_poll(self):
        """api deletes first poll on merge"""
        self.override_acl({'can_merge_threads': True})

        other_thread = testutils.post_thread(self.category)
        poll = testutils.post_poll(self.thread, self.user)
        other_poll = testutils.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({
                'threads': [self.thread.id, other_thread.id],
                'title': 'Merged thread!',
                'category': self.category.id,
                'poll': other_poll.pk,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # other poll and its votes are gone
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

        Poll.objects.get(pk=other_poll.pk)
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(pk=poll.pk)
