import json

from django.urls import reverse

from .. import test
from ...acl import useracl
from ...acl.objectacl import add_acl_to_obj
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...conftest import get_cache_versions
from ...readtracker import poststracker
from ..models import Poll, PollVote, Post, Thread
from ..serializers import ThreadsListSerializer
from ..test import patch_category_acl, patch_other_category_acl
from .test_threads_api import ThreadsApiTestCase

cache_versions = get_cache_versions()


class ThreadsMergeApiTests(ThreadsApiTestCase):
    def setUp(self):
        super().setUp()
        self.api_link = reverse("misago:api:thread-merge")

        Category(name="Other Category", slug="other-category").insert_at(
            self.category, position="last-child", save=True
        )
        self.other_category = Category.objects.get(slug="other-category")

    def test_merge_no_threads(self):
        """api validates if we are trying to merge no threads"""
        response = self.client.post(self.api_link, content_type="application/json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two threads to merge."},
        )

    def test_merge_empty_threads(self):
        """api validates if we are trying to empty threads list"""
        response = self.client.post(
            self.api_link, json.dumps({"threads": []}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two threads to merge."},
        )

    def test_merge_invalid_threads(self):
        """api validates if we are trying to merge invalid thread ids"""
        response = self.client.post(
            self.api_link,
            json.dumps({"threads": "abcd"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "str".'}
        )

        response = self.client.post(
            self.api_link,
            json.dumps({"threads": ["a", "-", "c"]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": ["One or more thread ids received were invalid."]},
        )

    def test_merge_single_thread(self):
        """api validates if we are trying to merge single thread"""
        response = self.client.post(
            self.api_link,
            json.dumps({"threads": [self.thread.id]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two threads to merge."},
        )

    def test_merge_with_nonexisting_thread(self):
        """api validates if we are trying to merge with invalid thread"""
        response = self.client.post(
            self.api_link,
            json.dumps({"threads": [self.thread.id, self.thread.id + 1000]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more threads to merge could not be found."},
        )

    def test_merge_with_invisible_thread(self):
        """api validates if we are trying to merge with inaccesible thread"""
        unaccesible_thread = test.post_thread(category=self.other_category)

        response = self.client.post(
            self.api_link,
            json.dumps({"threads": [self.thread.id, unaccesible_thread.id]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "One or more threads to merge could not be found."},
        )

    def test_merge_no_permission(self):
        """api validates permission to merge threads"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "category": self.category.id,
                    "title": "Lorem ipsum dolor",
                    "threads": [self.thread.id, thread.id],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": thread.pk,
                    "title": thread.title,
                    "errors": ["You can't merge threads in this category."],
                },
                {
                    "id": self.thread.pk,
                    "title": self.thread.title,
                    "errors": ["You can't merge threads in this category."],
                },
            ],
        )

    @patch_other_category_acl()
    @patch_category_acl({"can_merge_threads": True, "can_close_threads": False})
    def test_thread_category_is_closed(self):
        """api validates if thread's category is open"""
        other_thread = test.post_thread(self.category)

        self.category.is_closed = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "category": self.other_category.id,
                    "title": "Lorem ipsum dolor",
                    "threads": [self.thread.id, other_thread.id],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": other_thread.id,
                    "title": other_thread.title,
                    "errors": [
                        "This category is closed. You can't merge it's threads."
                    ],
                },
                {
                    "id": self.thread.id,
                    "title": self.thread.title,
                    "errors": [
                        "This category is closed. You can't merge it's threads."
                    ],
                },
            ],
        )

    @patch_other_category_acl()
    @patch_category_acl({"can_merge_threads": True, "can_close_threads": False})
    def test_thread_is_closed(self):
        """api validates if thread is open"""
        other_thread = test.post_thread(self.category)

        other_thread.is_closed = True
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "category": self.other_category.id,
                    "title": "Lorem ipsum dolor",
                    "threads": [self.thread.id, other_thread.id],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": other_thread.id,
                    "title": other_thread.title,
                    "errors": [
                        "This thread is closed. You can't merge it with other threads."
                    ],
                }
            ],
        )

    @override_dynamic_settings(threads_per_page=4)
    @patch_category_acl({"can_merge_threads": True})
    def test_merge_too_many_threads(self):
        """api rejects too many threads to merge"""
        threads = []
        for _ in range(5):
            threads.append(test.post_thread(category=self.category).pk)

        response = self.client.post(
            self.api_link,
            json.dumps({"threads": threads}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "No more than 4 threads can be merged at a single time."},
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_no_final_thread(self):
        """api rejects merge because no data to merge threads was specified"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({"threads": [self.thread.id, thread.id]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": ["This field is required."],
                "category": ["This field is required."],
            },
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_invalid_final_title(self):
        """api rejects merge because final thread title was invalid"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "$$$",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_invalid_category(self):
        """api rejects merge because final category was invalid"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.other_category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"category": ["Requested category could not be found."]}
        )

    @patch_category_acl({"can_merge_threads": True, "can_start_threads": False})
    def test_merge_unallowed_start_thread(self):
        """api rejects merge because category isn't allowing starting threads"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"category": ["You can't create new threads in selected category."]},
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_invalid_weight(self):
        """api rejects merge because final weight was invalid"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "weight": 4,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"weight": ["Ensure this value is less than or equal to 2."]},
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_unallowed_global_weight(self):
        """api rejects merge because global weight was unallowed"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "weight": 2,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "weight": [
                    "You don't have permission to pin threads globally "
                    "in this category."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_unallowed_local_weight(self):
        """api rejects merge because local weight was unallowed"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "weight": 1,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"weight": ["You don't have permission to pin threads in this category."]},
        )

    @patch_category_acl({"can_merge_threads": True, "can_pin_threads": 1})
    def test_merge_allowed_local_weight(self):
        """api allows local weight"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 1,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True, "can_pin_threads": 2})
    def test_merge_allowed_global_weight(self):
        """api allows global weight"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 2,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True, "can_close_threads": False})
    def test_merge_unallowed_close(self):
        """api rejects merge because closing thread was unallowed"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "is_closed": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "is_closed": [
                    "You don't have permission to close threads in this category."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True, "can_close_threads": True})
    def test_merge_with_close(self):
        """api allows for closing thread"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 0,
                    "is_closed": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True, "can_hide_threads": 0})
    def test_merge_unallowed_hidden(self):
        """api rejects merge because hidden thread was unallowed"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "is_hidden": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "is_hidden": [
                    "You don't have permission to hide threads in this category."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True, "can_hide_threads": 1})
    def test_merge_with_hide(self):
        """api allows for hiding thread"""
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 0,
                    "is_hidden": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_merge(self):
        """api performs basic merge"""
        posts_ids = [p.id for p in Post.objects.all()]
        thread = test.post_thread(category=self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # is response json with new thread?
        response_json = response.json()

        new_thread = Thread.objects.get(pk=response_json["id"])
        new_thread.is_read = False
        new_thread.subscription = None

        user_acl = useracl.get_user_acl(self.user, cache_versions)
        add_acl_to_obj(user_acl, new_thread.category)
        add_acl_to_obj(user_acl, new_thread)

        self.assertEqual(response_json, ThreadsListSerializer(new_thread).data)

        # did posts move to new thread?
        for post in Post.objects.filter(id__in=posts_ids):
            self.assertEqual(post.thread_id, new_thread.id)

        # are old threads gone?
        self.assertEqual([t.pk for t in Thread.objects.all()], [new_thread.pk])

    @patch_category_acl(
        {
            "can_merge_threads": True,
            "can_close_threads": True,
            "can_hide_threads": 1,
            "can_pin_threads": 2,
        }
    )
    def test_merge_kitchensink(self):
        """api performs merge"""
        posts_ids = [p.id for p in Post.objects.all()]
        thread = test.post_thread(category=self.category)

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
            json.dumps(
                {
                    "threads": [self.thread.id, thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "is_closed": 1,
                    "is_hidden": 1,
                    "weight": 2,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # is response json with new thread?
        response_json = response.json()

        new_thread = Thread.objects.get(pk=response_json["id"])
        new_thread.is_read = False
        new_thread.subscription = None

        self.assertEqual(new_thread.weight, 2)
        self.assertTrue(new_thread.is_closed)
        self.assertTrue(new_thread.is_hidden)

        user_acl = useracl.get_user_acl(self.user, cache_versions)
        add_acl_to_obj(user_acl, new_thread.category)
        add_acl_to_obj(user_acl, new_thread)

        self.assertEqual(response_json, ThreadsListSerializer(new_thread).data)

        # did posts move to new thread?
        for post in Post.objects.filter(id__in=posts_ids):
            self.assertEqual(post.thread_id, new_thread.id)

        # are old threads gone?
        self.assertEqual([t.pk for t in Thread.objects.all()], [new_thread.pk])

        # posts reads are kept
        postreads = self.user.postread_set.filter(post__is_event=False).order_by("id")

        self.assertEqual(
            list(postreads.values_list("post_id", flat=True)),
            [self.thread.first_post_id, thread.first_post_id],
        )
        self.assertEqual(postreads.filter(thread=new_thread).count(), 2)
        self.assertEqual(postreads.filter(category=self.category).count(), 2)

        # subscriptions are kept
        self.assertEqual(self.user.subscription_set.count(), 1)
        self.user.subscription_set.get(thread=new_thread)
        self.user.subscription_set.get(category=self.category)

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_merged_best_answer(self):
        """api merges two threads successfully, moving best answer to old thread"""
        other_thread = test.post_thread(self.category)

        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # best answer is set on new thread
        new_thread = Thread.objects.get(pk=response.json()["id"])
        self.assertEqual(new_thread.best_answer_id, best_answer.id)

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_merge_conflict_best_answer(self):
        """api errors on merge conflict, returning list of available best answers"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "best_answers": [
                    ["0", "Unmark all best answers"],
                    [str(self.thread.id), self.thread.title],
                    [str(other_thread.id), other_thread.title],
                ]
            },
        )

        # best answers were untouched
        self.assertEqual(self.thread.post_set.count(), 2)
        self.assertEqual(other_thread.post_set.count(), 2)
        self.assertEqual(
            Thread.objects.get(pk=self.thread.pk).best_answer_id, best_answer.id
        )
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, other_best_answer.id
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_best_answer_invalid_resolution(self):
        """api errors on invalid merge conflict resolution"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "best_answer": other_thread.id + 10,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"best_answer": ["Invalid choice."]})

        # best answers were untouched
        self.assertEqual(self.thread.post_set.count(), 2)
        self.assertEqual(other_thread.post_set.count(), 2)
        self.assertEqual(
            Thread.objects.get(pk=self.thread.pk).best_answer_id, best_answer.id
        )
        self.assertEqual(
            Thread.objects.get(pk=other_thread.pk).best_answer_id, other_best_answer.id
        )

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_unmark_all_best_answers(self):
        """api unmarks all best answers when unmark all choice is selected"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "best_answer": 0,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # best answer is not set on new thread
        new_thread = Thread.objects.get(pk=response.json()["id"])
        self.assertFalse(new_thread.has_best_answer)
        self.assertIsNone(new_thread.best_answer_id)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_first_best_answer(self):
        """api unmarks other best answer on merge"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "best_answer": self.thread.pk,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # selected best answer is set on new thread
        new_thread = Thread.objects.get(pk=response.json()["id"])
        self.assertEqual(new_thread.best_answer_id, best_answer.id)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_other_best_answer(self):
        """api unmarks first best answer on merge"""
        best_answer = test.reply_thread(self.thread)
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        other_thread = test.post_thread(self.category)
        other_best_answer = test.reply_thread(other_thread)
        other_thread.set_best_answer(self.user, other_best_answer)
        other_thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "best_answer": other_thread.pk,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # selected best answer is set on new thread
        new_thread = Thread.objects.get(pk=response.json()["id"])
        self.assertEqual(new_thread.best_answer_id, other_best_answer.id)

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_kept_poll(self):
        """api merges two threads successfully, keeping poll from other thread"""
        other_thread = test.post_thread(self.category)
        poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        new_thread = Thread.objects.get(pk=response.json()["id"])

        # poll and its votes were kept
        self.assertEqual(Poll.objects.filter(pk=poll.pk, thread=new_thread).count(), 1)
        self.assertEqual(
            PollVote.objects.filter(poll=poll, thread=new_thread).count(), 4
        )

        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

    @patch_category_acl({"can_merge_threads": True})
    def test_merge_threads_moved_poll(self):
        """api merges two threads successfully, moving poll from old thread"""
        other_thread = test.post_thread(self.category)
        poll = test.post_poll(self.thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        new_thread = Thread.objects.get(pk=response.json()["id"])

        # poll and its votes were kept
        self.assertEqual(Poll.objects.filter(pk=poll.pk, thread=new_thread).count(), 1)
        self.assertEqual(
            PollVote.objects.filter(poll=poll, thread=new_thread).count(), 4
        )

        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_poll(self):
        """api errors on merge conflict, returning list of available polls"""
        other_thread = test.post_thread(self.category)
        poll = test.post_poll(self.thread, self.user)
        other_poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "polls": [
                    ["0", "Delete all polls"],
                    [
                        str(other_poll.pk),
                        "%s (%s)" % (other_poll.question, other_poll.thread.title),
                    ],
                    [str(poll.pk), "%s (%s)" % (poll.question, poll.thread.title)],
                ]
            },
        )

        # polls and votes were untouched
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(PollVote.objects.count(), 8)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_poll_invalid_resolution(self):
        """api errors on invalid merge conflict resolution"""
        other_thread = test.post_thread(self.category)

        test.post_poll(self.thread, self.user)
        test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "poll": other_thread.poll.id + 10,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"poll": ["Invalid choice."]})

        # polls and votes were untouched
        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(PollVote.objects.count(), 8)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_delete_all_polls(self):
        """api deletes all polls when delete all choice is selected"""
        other_thread = test.post_thread(self.category)

        test.post_poll(self.thread, self.user)
        test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "poll": 0,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # polls and votes are gone
        self.assertEqual(Poll.objects.count(), 0)
        self.assertEqual(PollVote.objects.count(), 0)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_first_poll(self):
        """api deletes other poll on merge"""
        other_thread = test.post_thread(self.category)
        poll = test.post_poll(self.thread, self.user)
        other_poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "poll": poll.pk,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # other poll and its votes are gone
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

        Poll.objects.get(pk=poll.pk)
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(pk=other_poll.pk)

    @patch_category_acl({"can_merge_threads": True})
    def test_threads_merge_conflict_keep_other_poll(self):
        """api deletes first poll on merge"""
        other_thread = test.post_thread(self.category)
        poll = test.post_poll(self.thread, self.user)
        other_poll = test.post_poll(other_thread, self.user)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "threads": [self.thread.id, other_thread.id],
                    "title": "Merged thread!",
                    "category": self.category.id,
                    "poll": other_poll.pk,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # other poll and its votes are gone
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(PollVote.objects.count(), 4)

        Poll.objects.get(pk=other_poll.pk)
        with self.assertRaises(Poll.DoesNotExist):
            Poll.objects.get(pk=poll.pk)
