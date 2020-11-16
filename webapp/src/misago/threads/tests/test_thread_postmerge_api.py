import json

from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...readtracker import poststracker
from ...users.test import AuthenticatedUserTestCase
from ..models import Post
from ..test import patch_category_acl


class ThreadPostMergeApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)
        self.post = test.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            "misago:api:thread-post-merge", kwargs={"thread_pk": self.thread.pk}
        )

    def test_anonymous_user(self):
        """you need to authenticate to merge posts"""
        self.logout_user()

        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This action is not available to guests."}
        )

    @patch_category_acl({"can_merge_posts": False})
    def test_no_permission(self):
        """api validates permission to merge"""
        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't merge posts in this thread."}
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_empty_data_json(self):
        """api handles empty json data"""
        response = self.client.post(
            self.api_link, json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two posts to merge."},
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_empty_data_form(self):
        """api handles empty form data"""
        response = self.client.post(self.api_link, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two posts to merge."},
        )

    @patch_category_acl({"can_merge_posts": True})
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

    @patch_category_acl({"can_merge_posts": True})
    def test_no_posts_ids(self):
        """api rejects no posts ids"""
        response = self.client.post(
            self.api_link, json.dumps({"posts": []}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two posts to merge."},
        )

    @patch_category_acl({"can_merge_posts": True})
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

    @patch_category_acl({"can_merge_posts": True})
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

    @patch_category_acl({"can_merge_posts": True})
    def test_one_post_id(self):
        """api rejects one post id"""
        response = self.client.post(
            self.api_link, json.dumps({"posts": [1]}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "You have to select at least two posts to merge."},
        )

    @override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=3)
    @patch_category_acl({"can_merge_posts": True})
    def test_merge_limit(self):
        """api rejects more posts than merge limit"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": list(range(9))}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "No more than 8 posts can be merged at a single time."},
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_event(self):
        """api recjects events"""
        event = test.reply_thread(self.thread, is_event=True, poster=self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.post.pk, event.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Events can't be merged."})

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_notfound_pk(self):
        """api recjects nonexistant pk's"""
        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.post.pk, self.post.pk * 1000]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to merge could not be found."},
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_cross_threads(self):
        """api recjects attempt to merge with post made in other thread"""
        other_thread = test.post_thread(category=self.category)
        other_post = test.reply_thread(other_thread, poster=self.user)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.post.pk, other_post.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "One or more posts to merge could not be found."},
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_authenticated_with_guest_post(self):
        """api recjects attempt to merge with post made by deleted user"""
        other_post = test.reply_thread(self.thread)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.post.pk, other_post.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Posts made by different users can't be merged."},
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_guest_with_authenticated_post(self):
        """api recjects attempt to merge with post made by deleted user"""
        other_post = test.reply_thread(self.thread)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [other_post.pk, self.post.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Posts made by different users can't be merged."},
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_guest_posts_different_usernames(self):
        """api recjects attempt to merge posts made by different guests"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(self.thread, poster="Bob").pk,
                        test.reply_thread(self.thread, poster="Miku").pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Posts made by different users can't be merged."},
        )

    @patch_category_acl({"can_merge_posts": True, "can_hide_posts": 1})
    def test_merge_different_visibility(self):
        """api recjects attempt to merge posts with different visibility"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(
                            self.thread, poster=self.user, is_hidden=True
                        ).pk,
                        test.reply_thread(
                            self.thread, poster=self.user, is_hidden=False
                        ).pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Posts with different visibility can't be merged."},
        )

    @patch_category_acl({"can_merge_posts": True, "can_approve_content": True})
    def test_merge_different_approval(self):
        """api recjects attempt to merge posts with different approval"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(
                            self.thread, poster=self.user, is_unapproved=True
                        ).pk,
                        test.reply_thread(
                            self.thread, poster=self.user, is_unapproved=False
                        ).pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Posts with different visibility can't be merged."},
        )

    @patch_category_acl({"can_merge_posts": True, "can_close_threads": False})
    def test_closed_thread_no_permission(self):
        """api validates permission to merge in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        posts = [
            test.reply_thread(self.thread, poster=self.user).pk,
            test.reply_thread(self.thread, poster=self.user).pk,
        ]

        response = self.client.post(
            self.api_link, json.dumps({"posts": posts}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't merge posts in it."},
        )

    @patch_category_acl({"can_merge_posts": True, "can_close_threads": True})
    def test_closed_thread(self):
        """api validates permission to merge in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        posts = [
            test.reply_thread(self.thread, poster=self.user).pk,
            test.reply_thread(self.thread, poster=self.user).pk,
        ]

        response = self.client.post(
            self.api_link, json.dumps({"posts": posts}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_merge_posts": True, "can_close_threads": False})
    def test_closed_category_no_permission(self):
        """api validates permission to merge in closed category"""
        self.category.is_closed = True
        self.category.save()

        posts = [
            test.reply_thread(self.thread, poster=self.user).pk,
            test.reply_thread(self.thread, poster=self.user).pk,
        ]

        response = self.client.post(
            self.api_link, json.dumps({"posts": posts}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't merge posts in it."},
        )

    @patch_category_acl({"can_merge_posts": True, "can_close_threads": True})
    def test_closed_category(self):
        """api validates permission to merge in closed category"""
        self.category.is_closed = True
        self.category.save()

        posts = [
            test.reply_thread(self.thread, poster=self.user).pk,
            test.reply_thread(self.thread, poster=self.user).pk,
        ]

        response = self.client.post(
            self.api_link, json.dumps({"posts": posts}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_best_answer_first_post(self):
        """api recjects attempt to merge best_answer with first post"""
        self.thread.first_post.poster = self.user
        self.thread.first_post.save()

        self.post.poster = self.user
        self.post.save()

        self.thread.set_best_answer(self.user, self.post)
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.thread.first_post.pk, self.post.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": (
                    "Post marked as best answer can't be "
                    "merged with thread's first post."
                )
            },
        )

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_posts(self):
        """api merges two posts"""
        post_a = test.reply_thread(self.thread, poster=self.user, message="Battęry")
        post_b = test.reply_thread(self.thread, poster=self.user, message="Hórse")

        thread_replies = self.thread.replies

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [post_a.pk, post_b.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.replies, thread_replies - 1)

        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post_b.pk)

        merged_post = Post.objects.get(pk=post_a.pk)
        self.assertEqual(merged_post.parsed, "%s\n%s" % (post_a.parsed, post_b.parsed))

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_guest_posts(self):
        """api recjects attempt to merge posts made by same guest"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(self.thread, poster="Bob").pk,
                        test.reply_thread(self.thread, poster="Bob").pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_merge_posts": True, "can_hide_posts": 1})
    def test_merge_hidden_posts(self):
        """api merges two hidden posts"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(
                            self.thread, poster=self.user, is_hidden=True
                        ).pk,
                        test.reply_thread(
                            self.thread, poster=self.user, is_hidden=True
                        ).pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_merge_posts": True, "can_approve_content": True})
    def test_merge_unapproved_posts(self):
        """api merges two unapproved posts"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(
                            self.thread, poster=self.user, is_unapproved=True
                        ).pk,
                        test.reply_thread(
                            self.thread, poster=self.user, is_unapproved=True
                        ).pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_merge_posts": True, "can_hide_threads": True})
    def test_merge_with_hidden_thread(self):
        """api excludes thread's first post from visibility checks"""
        self.thread.first_post.is_hidden = True
        self.thread.first_post.poster = self.user
        self.thread.first_post.save()

        post_visible = test.reply_thread(self.thread, poster=self.user, is_hidden=False)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [self.thread.first_post.pk, post_visible.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_protected(self):
        """api preserves protected status after merge"""
        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        test.reply_thread(
                            self.thread, poster="Bob", is_protected=True
                        ).pk,
                        test.reply_thread(
                            self.thread, poster="Bob", is_protected=False
                        ).pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        merged_post = self.thread.post_set.order_by("-id")[0]
        self.assertTrue(merged_post.is_protected)

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_best_answer(self):
        """api merges best answer with other post"""
        best_answer = test.reply_thread(self.thread, poster="Bob")

        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        best_answer.pk,
                        test.reply_thread(self.thread, poster="Bob").pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.best_answer, best_answer)

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_best_answer_in(self):
        """api merges best answer into other post"""
        other_post = test.reply_thread(self.thread, poster="Bob")
        best_answer = test.reply_thread(self.thread, poster="Bob")

        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [best_answer.pk, other_post.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.best_answer, other_post)

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_best_answer_in_protected(self):
        """api merges best answer into protected post"""
        best_answer = test.reply_thread(self.thread, poster="Bob")

        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        response = self.client.post(
            self.api_link,
            json.dumps(
                {
                    "posts": [
                        best_answer.pk,
                        test.reply_thread(
                            self.thread, poster="Bob", is_protected=True
                        ).pk,
                    ]
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.thread.refresh_from_db()
        self.assertEqual(self.thread.best_answer, best_answer)

        self.thread.best_answer.refresh_from_db()
        self.assertTrue(self.thread.best_answer.is_protected)
        self.assertTrue(self.thread.best_answer_is_protected)

    @patch_category_acl({"can_merge_posts": True})
    def test_merge_remove_reads(self):
        """two posts merge removes read tracker from post"""
        post_a = test.reply_thread(self.thread, poster=self.user, message="Battęry")
        post_b = test.reply_thread(self.thread, poster=self.user, message="Hórse")

        poststracker.save_read(self.user, post_a)
        poststracker.save_read(self.user, post_b)

        response = self.client.post(
            self.api_link,
            json.dumps({"posts": [post_a.pk, post_b.pk]}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        # both post's were removed from readtracker
        self.assertEqual(self.user.postread_set.count(), 0)
