import json

from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...readtracker import poststracker
from ...users.test import AuthenticatedUserTestCase
from ..models import Thread
from ..test import patch_category_acl, patch_other_category_acl


class ThreadPostMoveApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)

        self.api_link = reverse(
            "misago:api:thread-post-move", kwargs={"thread_pk": self.thread.pk}
        )

        Category(name="Other category", slug="other-category").insert_at(
            self.category, position="last-child", save=True
        )
        self.other_category = Category.objects.get(slug="other-category")

    def test_anonymous_user(self):
        """you need to authenticate to move posts"""
        self.logout_user()

        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
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
            {"detail": "Invalid data. Expected a dictionary, but got list."},
        )

        response = self.client.post(
            self.api_link, "123", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Invalid data. Expected a dictionary, but got int."},
        )

        response = self.client.post(
            self.api_link, '"string"', content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Invalid data. Expected a dictionary, but got str."},
        )

        response = self.client.post(
            self.api_link, "malformed", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"},
        )

    @patch_category_acl({"can_move_posts": False})
    def test_no_permission(self):
        """api validates permission to move"""
        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't move posts in this thread."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_move_no_new_thread_url(self):
        """api validates if new thread url was given"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Enter link to new thread."})

    @patch_category_acl({"can_move_posts": True})
    def test_invalid_new_thread_url(self):
        """api validates new thread url"""
        response = self.client.post(
            self.api_link, {"new_thread": self.user.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "This is not a valid thread link."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_current_new_thread_url(self):
        """api validates if new thread url points to current thread"""
        response = self.client.post(
            self.api_link, {"new_thread": self.thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Thread to move posts to is same as current one."},
        )

    @patch_other_category_acl({"can_see": False})
    @patch_category_acl({"can_move_posts": True})
    def test_other_thread_exists(self):
        """api validates if other thread exists"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"new_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "The thread you have entered link to doesn't exist "
                    "or you don't have permission to see it."
                )
            },
        )

    @patch_other_category_acl({"can_browse": False})
    @patch_category_acl({"can_move_posts": True})
    def test_other_thread_is_invisible(self):
        """api validates if other thread is visible"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"new_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "The thread you have entered link to doesn't exist "
                    "or you don't have permission to see it."
                )
            },
        )

    @patch_other_category_acl({"can_reply_threads": False})
    @patch_category_acl({"can_move_posts": True})
    def test_other_thread_isnt_replyable(self):
        """api validates if other thread can be replied"""
        other_thread = test.post_thread(self.other_category)

        response = self.client.post(
            self.api_link, {"new_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You can't move posts to threads you can't reply."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_empty_data(self):
        """api handles empty data"""
        test.post_thread(self.category)

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Enter link to new thread."})

    @patch_category_acl({"can_move_posts": True})
    def test_empty_posts_data_json(self):
        """api handles empty json data"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({"new_thread": other_thread.get_absolute_url()}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to move."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_empty_posts_data_form(self):
        """api handles empty form data"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link, {"new_thread": other_thread.get_absolute_url()}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to move."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps({"new_thread": other_thread.get_absolute_url(), "posts": []}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to specify at least one post to move."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_invalid_posts_data(self):
        """api handles invalid data"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {"new_thread": other_thread.get_absolute_url(), "posts": "string"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "str".'}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_invalid_posts_ids(self):
        """api handles invalid post id"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [1, 2, "string"],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "One or more post ids received were invalid."}
        )

    @override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=3)
    @patch_category_acl({"can_move_posts": True})
    def test_move_limit(self):
        """api rejects more posts than move limit"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {"new_thread": other_thread.get_absolute_url(), "posts": list(range(9))}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "No more than 8 posts can be moved at a single time."},
        )

    @patch_category_acl({"can_move_posts": True})
    def test_move_invisible(self):
        """api validates posts visibility"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [test.reply_thread(self.thread, is_unapproved=True).pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "One or more posts to move could not be found."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_move_other_thread_posts(self):
        """api recjects attempt to move other thread's post"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [test.reply_thread(other_thread, is_hidden=True).pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "One or more posts to move could not be found."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_move_event(self):
        """api rejects events move"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [test.reply_thread(self.thread, is_event=True).pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Events can't be moved."})

    @patch_category_acl({"can_move_posts": True})
    def test_move_first_post(self):
        """api rejects first post move"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [self.thread.first_post_id],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "You can't move thread's first post."}
        )

    @patch_category_acl({"can_move_posts": True})
    def test_move_hidden_posts(self):
        """api recjects attempt to move urneadable hidden post"""
        other_thread = test.post_thread(self.category)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [test.reply_thread(self.thread, is_hidden=True).pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You can't move posts the content you can't see."},
        )

    @patch_category_acl({"can_move_posts": True, "can_close_threads": False})
    def test_move_posts_closed_thread_no_permission(self):
        """api recjects attempt to move posts from closed thread"""
        other_thread = test.post_thread(self.category)

        self.thread.is_closed = True
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [test.reply_thread(self.thread).pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't move posts in it."},
        )

    @patch_other_category_acl({"can_reply_threads": True, "can_close_threads": False})
    @patch_category_acl({"can_move_posts": True})
    def test_move_posts_closed_category_no_permission(self):
        """api recjects attempt to move posts from closed thread"""
        other_thread = test.post_thread(self.other_category)

        self.category.is_closed = True
        self.category.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [test.reply_thread(self.thread).pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't move posts in it."},
        )

    @patch_other_category_acl({"can_reply_threads": True})
    @patch_category_acl({"can_move_posts": True})
    def test_move_posts(self):
        """api moves posts to other thread"""
        other_thread = test.post_thread(self.other_category)

        posts = (
            test.reply_thread(self.thread).pk,
            test.reply_thread(self.thread).pk,
            test.reply_thread(self.thread).pk,
            test.reply_thread(self.thread).pk,
        )

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 4)

        response = self.client.post(
            self.api_link,
            json.dumps({"new_thread": other_thread.get_absolute_url(), "posts": posts}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # replies were moved
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 0)

        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.post_set.filter(pk__in=posts).count(), 4)
        self.assertEqual(other_thread.replies, 4)

    @patch_other_category_acl({"can_reply_threads": True})
    @patch_category_acl({"can_move_posts": True})
    def test_move_best_answer(self):
        """api moves best answer to other thread"""
        other_thread = test.post_thread(self.other_category)
        best_answer = test.reply_thread(self.thread)

        self.thread.set_best_answer(self.user, best_answer)
        self.thread.synchronize()
        self.thread.save()

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.best_answer, best_answer)
        self.assertEqual(self.thread.replies, 1)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [best_answer.pk],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # best_answer was moved and unmarked
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 0)
        self.assertIsNone(self.thread.best_answer)

        other_thread = Thread.objects.get(pk=other_thread.pk)
        self.assertEqual(other_thread.replies, 1)
        self.assertIsNone(other_thread.best_answer)

    @patch_other_category_acl({"can_reply_threads": True})
    @patch_category_acl({"can_move_posts": True})
    def test_move_posts_reads(self):
        """api moves posts reads together with posts"""
        other_thread = test.post_thread(self.other_category)

        posts = (test.reply_thread(self.thread), test.reply_thread(self.thread))

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, 2)

        poststracker.save_read(self.user, self.thread.first_post)
        for post in posts:
            poststracker.save_read(self.user, post)

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "new_thread": other_thread.get_absolute_url(),
                    "posts": [p.pk for p in posts],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        other_thread = Thread.objects.get(pk=other_thread.pk)

        # postreads were removed
        postreads = self.user.postread_set.order_by("id")

        postreads_threads = list(postreads.values_list("thread_id", flat=True))
        self.assertEqual(postreads_threads, [self.thread.pk])

        postreads_categories = list(postreads.values_list("category_id", flat=True))
        self.assertEqual(postreads_categories, [self.category.pk])
