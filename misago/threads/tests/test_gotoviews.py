from django.utils import timezone

from .. import test
from ...categories.models import Category
from ...conf.test import override_dynamic_settings
from ...readtracker.poststracker import save_read
from ...users.test import AuthenticatedUserTestCase
from ..test import patch_category_acl

GOTO_URL = "%s#post-%s"
GOTO_PAGE_URL = "%s%s/#post-%s"

POSTS_PER_PAGE = 7
POSTS_PER_PAGE_ORPHANS = 3


class GotoViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")
        self.thread = test.post_thread(category=self.category)


class GotoPostTests(GotoViewTestCase):
    def test_goto_first_post(self):
        """first post redirect url is valid"""
        response = self.client.get(self.thread.first_post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id),
        )

        response = self.client.get(response["location"])
        self.assertContains(response, self.thread.first_post.get_absolute_url())

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_last_post_on_page(self):
        """last post on page redirect url is valid"""
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS - 1):
            post = test.reply_thread(self.thread)

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"], GOTO_URL % (self.thread.get_absolute_url(), post.pk)
        )

        response = self.client.get(response["location"])
        self.assertContains(response, post.get_absolute_url())

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_first_post_on_next_page(self):
        """first post on next page redirect url is valid"""
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS):
            post = test.reply_thread(self.thread)

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk),
        )

        response = self.client.get(response["location"])
        self.assertContains(response, post.get_absolute_url())

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_first_post_on_page_three_out_of_five(self):
        """first post on next page redirect url is valid"""
        posts = []
        for _ in range(POSTS_PER_PAGE * 4 - 1):
            post = test.reply_thread(self.thread)
            posts.append(post)

        post = posts[POSTS_PER_PAGE * 2 - 3]

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 3, post.pk),
        )

        response = self.client.get(response["location"])
        self.assertContains(response, post.get_absolute_url())

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_first_event_on_page_three_out_of_five(self):
        """event redirect url is valid"""
        posts = []
        for _ in range(POSTS_PER_PAGE * 4 - 1):
            post = test.reply_thread(self.thread)
            posts.append(post)

        post = posts[POSTS_PER_PAGE * 2 - 2]

        self.thread.has_events = True
        self.thread.save()

        post.is_event = True
        post.save()

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 3, post.pk),
        )

        response = self.client.get(response["location"])
        self.assertContains(response, post.get_absolute_url())


class GotoLastTests(GotoViewTestCase):
    def test_goto_last_post(self):
        """first post redirect url is valid"""
        response = self.client.get(self.thread.get_last_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id),
        )

        response = self.client.get(response["location"])
        self.assertContains(response, self.thread.last_post.get_absolute_url())

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_last_post_on_page(self):
        """last post on page redirect url is valid"""
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS - 1):
            post = test.reply_thread(self.thread)

        response = self.client.get(self.thread.get_last_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"], GOTO_URL % (self.thread.get_absolute_url(), post.pk)
        )

        response = self.client.get(response["location"])
        self.assertContains(response, post.get_absolute_url())


class GotoNewTests(GotoViewTestCase):
    def test_goto_first_post(self):
        """first unread post redirect url is valid"""
        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id),
        )

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_first_new_post(self):
        """first unread post redirect url in already read thread is valid"""
        save_read(self.user, self.thread.first_post)

        post = test.reply_thread(self.thread, posted_on=timezone.now())
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS - 1):
            test.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"], GOTO_URL % (self.thread.get_absolute_url(), post.pk)
        )

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_first_new_post_on_next_page(self):
        """first unread post redirect url in already read multipage thread is valid"""
        save_read(self.user, self.thread.first_post)

        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS):
            last_post = test.reply_thread(self.thread, posted_on=timezone.now())
            save_read(self.user, last_post)

        post = test.reply_thread(self.thread, posted_on=timezone.now())
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS - 1):
            test.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk),
        )

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_goto_first_new_post_in_read_thread(self):
        """goto new in read thread points to last post"""
        save_read(self.user, self.thread.first_post)

        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS):
            post = test.reply_thread(self.thread, posted_on=timezone.now())
            save_read(self.user, post)

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk),
        )

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_guest_goto_first_new_post_in_thread(self):
        """guest goto new in read thread points to last post"""
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS):
            post = test.reply_thread(self.thread, posted_on=timezone.now())

        self.logout_user()

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk),
        )


class GotoBestAnswerTests(GotoViewTestCase):
    def test_view_handles_no_best_answer(self):
        """if thread has no best answer, redirect to first post"""
        response = self.client.get(self.thread.get_best_answer_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id),
        )

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    def test_view_handles_best_answer(self):
        """if thread has best answer, redirect to it"""
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS):
            test.reply_thread(self.thread, posted_on=timezone.now())

        best_answer = test.reply_thread(self.thread, posted_on=timezone.now())
        self.thread.set_best_answer(self.user, best_answer)
        self.thread.save()

        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS - 1):
            test.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.get(self.thread.get_best_answer_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, best_answer.pk),
        )


class GotoUnapprovedTests(GotoViewTestCase):
    def test_view_validates_permission(self):
        """view validates permission to see unapproved posts"""
        response = self.client.get(self.thread.get_unapproved_post_url())
        self.assertContains(
            response, "You need permission to approve content", status_code=403
        )

        with patch_category_acl({"can_approve_content": True}):
            response = self.client.get(self.thread.get_unapproved_post_url())
            self.assertEqual(response.status_code, 302)

    @patch_category_acl({"can_approve_content": True})
    def test_view_handles_no_unapproved_posts(self):
        """if thread has no unapproved posts, redirect to last post"""
        response = self.client.get(self.thread.get_unapproved_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id),
        )

    @override_dynamic_settings(
        posts_per_page=POSTS_PER_PAGE, posts_per_page_orphans=POSTS_PER_PAGE_ORPHANS
    )
    @patch_category_acl({"can_approve_content": True})
    def test_view_handles_unapproved_posts(self):
        """if thread has unapproved posts, redirect to first of them"""
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS):
            test.reply_thread(self.thread, posted_on=timezone.now())

        post = test.reply_thread(
            self.thread, is_unapproved=True, posted_on=timezone.now()
        )
        for _ in range(POSTS_PER_PAGE + POSTS_PER_PAGE_ORPHANS - 1):
            test.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.get(self.thread.get_unapproved_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["location"],
            GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk),
        )


class ThreadGotoPostTests(GotoViewTestCase):
    """brureforcing regression tests for regression test for #869"""

    def test_thread_growing_post_goto(self):
        """growing thread goto views don't fail"""
        for _ in range(60):
            post = test.reply_thread(self.thread, posted_on=timezone.now())

            # go to post link is valid
            post_url = self.client.get(post.get_absolute_url())["location"]

            response = self.client.get(post_url)
            self.assertContains(response, post.get_absolute_url())

            # go to last post link is valid
            last_url = self.client.get(self.thread.get_last_post_url())["location"]
            self.assertEqual(post_url, last_url)

    def test_thread_growing_event_goto(self):
        """growing thread goto views don't fail for events"""
        for i in range(60):
            test.reply_thread(self.thread, posted_on=timezone.now())

            post = test.reply_thread(self.thread, posted_on=timezone.now())
            post.is_event = True
            post.save()

            # go to post link is valid
            post_url = self.client.get(post.get_absolute_url())["location"]

            if i == 0:
                # manually set events flag after first event was created
                self.thread.has_events = True
                self.thread.save()

            response = self.client.get(post_url)
            self.assertContains(response, post.get_absolute_url())

            # go to last post link is valid
            last_url = self.client.get(self.thread.get_last_post_url())["location"]
            self.assertEqual(post_url, last_url)

    def test_thread_post_goto(self):
        """thread goto views don't fail"""
        for _ in range(60):
            test.reply_thread(self.thread, posted_on=timezone.now())

        for post in self.thread.post_set.order_by("id").iterator():
            # go to post link is valid
            post_url = self.client.get(post.get_absolute_url())["location"]

            response = self.client.get(post_url)
            self.assertContains(response, post.get_absolute_url())

        # go to last post link is valid
        last_url = self.client.get(self.thread.get_last_post_url())["location"]
        self.assertEqual(post_url, last_url)

    def test_thread_event_goto(self):
        """thread goto views don't fail for events"""
        for _ in range(60):
            test.reply_thread(self.thread, posted_on=timezone.now())

            post = test.reply_thread(self.thread, posted_on=timezone.now())
            post.is_event = True
            post.save()

        for post in (
            self.thread.post_set.filter(is_event=True).order_by("id").iterator()
        ):
            # go to post link is valid
            post_url = self.client.get(post.get_absolute_url())["location"]

            response = self.client.get(post_url)
            self.assertContains(response, post.get_absolute_url())

        # go to last post link is valid
        last_url = self.client.get(self.thread.get_last_post_url())["location"]
        self.assertEqual(post_url, last_url)
