import json

from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...readtracker import poststracker
from ...users.test import AuthenticatedUserTestCase
from ..models import Post
from ..test import patch_category_acl, patch_other_category_acl


class ThreadPostSplitApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)
        self.posts = [
            test.reply_thread(self.thread).pk,
            test.reply_thread(self.thread).pk,
        ]

        self.api_link = reverse(
            "misago:api:thread-post-split", kwargs={"thread_pk": self.thread.pk}
        )

        Category(name="Other category", slug="other-category").insert_at(
            self.category, position="last-child", save=True
        )
        self.other_category = Category.objects.get(slug="other-category")

    def test_anonymous_user(self):
        """you need to authenticate to split posts"""
        self.logout_user()

        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    @patch_category_acl({"can_move_posts": False})
    def test_no_permission(self):
        """api validates permission to split"""
        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't split posts from this thread."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_empty_data(self):
        """api handles empty data"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to split."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_invalid_data(self):
        """api handles post that is invalid type"""
        response = self.client.post(
            self.api_link, "[]", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got list."
                ]
            },
        )

        response = self.client.post(
            self.api_link, "123", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Invalid data. Expected a dictionary, but got int."]},
        )

        response = self.client.post(
            self.api_link, '"string"', content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Invalid data. Expected a dictionary, but got str."]},
        )

        response = self.client.post(
            self.api_link, "malformed", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to split."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_empty_posts_ids(self):
        """api rejects empty posts ids list"""
        response = self.client.post(
            self.api_link, json.dumps({"posts": []}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to split."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_invalid_posts_data(self):
        """api handles invalid data"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": "string"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "str".'}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_invalid_posts_ids(self):
        """api handles invalid post id"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [1, 2, "string"]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "One or more post ids received were invalid."}
        )

    @override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=3)
    @patch_category_acl({"can_move_posts": True})
    def test_split_limit(self):
        """api rejects more posts than split limit"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": list(range(9))}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "No more than 8 posts can be split at a single time."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_invisible(self):
        """api validates posts visibility"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {"posts": [test.reply_thread(self.thread, is_unapproved=True).pk]}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to split could not be found."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_event(self):
        """api rejects events split"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [test.reply_thread(self.thread, is_event=True).pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Events can't be split."})

    @patch_category_acl({"can_move_posts": True})
    def test_split_first_post(self):
        """api rejects first post split"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.thread.first_post_id]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "You can't split thread's first post."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_hidden_posts(self):
        """api recjects attempt to split urneadable hidden post"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [test.reply_thread(self.thread, is_hidden=True).pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You can't split posts the content you can't see."},
        )

    @patch_category_acl({"can_move_posts": True, "can_close_threads": False})
    def test_split_posts_closed_thread_no_permission(self):
        """api recjects attempt to split posts from closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [test.reply_thread(self.thread).pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't split posts in it."},
        )

    @patch_category_acl({"can_move_posts": True, "can_close_threads": False})
    def test_split_posts_closed_category_no_permission(self):
        """api recjects attempt to split posts from closed thread"""
        self.category.is_closed = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [test.reply_thread(self.thread).pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't split posts in it."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_other_thread_posts(self):
        """api recjects attempt to split other thread's post"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [test.reply_thread(other_thread, is_hidden=True).pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to split could not be found."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_empty_new_thread_data(self):
        """api handles empty form data"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": self.posts}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "title": ["This field is required."],
                "category": ["This field is required."],
            },
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_invalid_final_title(self):
        """api rejects split because final thread title was invalid"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {"posts": self.posts, "title": "$$$", "category": self.category.id}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_other_category_acl({"can_see": False})
    @patch_category_acl({"can_move_posts": True})
    def test_split_invalid_category(self):
        """api rejects split because final category was invalid"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.other_category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {"category": ["Requested category could not be found."]}
        )

    @patch_category_acl({"can_move_posts": True, "can_start_threads": False})
    def test_split_unallowed_start_thread(self):
        """api rejects split because category isn't allowing starting threads"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {"category": ["You can't create new threads in selected category."]},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_invalid_weight(self):
        """api rejects split because final weight was invalid"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "weight": 4,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json, {"weight": ["Ensure this value is less than or equal to 2."]}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split_unallowed_global_weight(self):
        """api rejects split because global weight was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "weight": 2,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "weight": [
                    "You don't have permission to pin threads "
                    "globally in this category."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True, "can_pin_threads": 0})
    def test_split_unallowed_local_weight(self):
        """api rejects split because local weight was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "weight": 1,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {"weight": ["You don't have permission to pin threads in this category."]},
        )

    @patch_category_acl({"can_move_posts": True, "can_pin_threads": 1})
    def test_split_allowed_local_weight(self):
        """api allows local weight"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 1,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True, "can_pin_threads": 2})
    def test_split_allowed_global_weight(self):
        """api allows global weight"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 2,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True, "can_close_threads": False})
    def test_split_unallowed_close(self):
        """api rejects split because closing thread was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "is_closed": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "is_closed": [
                    "You don't have permission to close threads in this category."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True, "can_close_threads": True})
    def test_split_with_close(self):
        """api allows for closing thread"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 0,
                    "is_closed": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True, "can_hide_threads": 0})
    def test_split_unallowed_hidden(self):
        """api rejects split because hidden thread was unallowed"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Valid thread title",
                    "category": self.category.id,
                    "is_hidden": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "is_hidden": [
                    "You don't have permission to hide threads in this category."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True, "can_hide_threads": 1})
    def test_split_with_hide(self):
        """api allows for hiding thread"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "$$$",
                    "category": self.category.id,
                    "weight": 0,
                    "is_hidden": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "title": [
                    "Thread title should be at least 5 characters long (it has 3)."
                ]
            },
        )

    @patch_category_acl({"can_move_posts": True})
    def test_split(self):
        """api splits posts to new thread"""
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 2)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Split thread.",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # thread was created
        split_thread = self.category.thread_set.get(slug="split-thread")
        self.assertEqual(split_thread.replies, 1)

        # posts were removed from old thread
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 0)

        # posts were moved to new thread
        self.assertEqual(split_thread.post_set.filter(pk__in=self.posts).count(), 2)

    @patch_category_acl({"can_move_posts": True})
    def test_split_best_answer(self):
        """api splits best answer to new thread"""
        best_answer = test.reply_thread(self.thread)

        self.thread.set_best_answer(self.user, best_answer)
        self.thread.synchronize()
        self.thread.save()

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.best_answer, best_answer)
        self.assertEqual(self.thread.replies, 3)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [best_answer.pk],
                    "title": "Split thread.",
                    "category": self.category.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # best_answer was moved and unmarked
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 2)
        self.assertIsNone(self.thread.best_answer)

        split_thread = self.category.thread_set.get(slug="split-thread")
        self.assertEqual(split_thread.replies, 0)
        self.assertIsNone(split_thread.best_answer)

    @patch_other_category_acl(
        {
            "can_start_threads": True,
            "can_close_threads": True,
            "can_hide_threads": True,
            "can_pin_threads": 2,
        }
    )
    @patch_category_acl({"can_move_posts": True})
    def test_split_kitchensink(self):
        """api splits posts with kitchensink"""
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 2)

        poststracker.save_read(self.user, self.thread.first_post)
        for post in self.posts:
            poststracker.save_read(
                self.user, Post.objects.select_related().get(pk=post)
            )

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": self.posts,
                    "title": "Split thread",
                    "category": self.other_category.id,
                    "weight": 2,
                    "is_closed": 1,
                    "is_hidden": 1,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # thread was created
        split_thread = self.other_category.thread_set.get(slug="split-thread")
        self.assertEqual(split_thread.replies, 1)
        self.assertEqual(split_thread.weight, 2)
        self.assertTrue(split_thread.is_closed)
        self.assertTrue(split_thread.is_hidden)

        # posts were removed from old thread
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 0)

        # posts were moved to new thread
        self.assertEqual(split_thread.post_set.filter(pk__in=self.posts).count(), 2)

        # postreads were removed
        postreads = self.user.postread_set.filter(post__is_event=False).order_by("id")

        postreads_threads = list(postreads.values_list("thread_id", flat=True))
        self.assertEqual(postreads_threads, [self.thread.pk])

        postreads_categories = list(postreads.values_list("category_id", flat=True))
        self.assertEqual(postreads_categories, [self.category.pk])
