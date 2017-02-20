from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.conf import settings
from misago.readtracker.threadstracker import make_thread_read_aware, read_thread
from misago.threads import testutils
from misago.users.testutils import AuthenticatedUserTestCase


GOTO_URL = '%s#post-%s'
GOTO_PAGE_URL = '%s%s/#post-%s'


class GotoViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(GotoViewTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)


class GotoPostTests(GotoViewTestCase):
    def test_goto_first_post(self):
        """first post redirect url is valid"""
        response = self.client.get(self.thread.first_post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, self.thread.first_post.get_absolute_url())

    def test_goto_last_post_on_page(self):
        """last post on page redirect url is valid"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL - 1):
            post = testutils.reply_thread(self.thread)

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_URL % (self.thread.get_absolute_url(), post.pk)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, post.get_absolute_url())

    def test_goto_first_post_on_next_page(self):
        """first post on next page redirect url is valid"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL):
            post = testutils.reply_thread(self.thread)

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, post.get_absolute_url())

    def test_goto_first_post_on_page_three_out_of_five(self):
        """first post on next page redirect url is valid"""
        posts = []
        for _ in range(settings.MISAGO_POSTS_PER_PAGE * 4 - 1):
            post = testutils.reply_thread(self.thread)
            posts.append(post)

        post = posts[settings.MISAGO_POSTS_PER_PAGE * 2 - 3]

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 3, post.pk)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, post.get_absolute_url())

    def test_goto_first_event_on_page_three_out_of_five(self):
        """event redirect url is valid"""
        posts = []
        for _ in range(settings.MISAGO_POSTS_PER_PAGE * 4 - 1):
            post = testutils.reply_thread(self.thread)
            posts.append(post)

        post = posts[settings.MISAGO_POSTS_PER_PAGE * 2 - 2]

        self.thread.has_events = True
        self.thread.save()

        post.is_event = True
        post.save()

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 3, post.pk)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, post.get_absolute_url())


class GotoLastTests(GotoViewTestCase):
    def test_goto_last_post(self):
        """first post redirect url is valid"""
        response = self.client.get(self.thread.get_last_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, self.thread.last_post.get_absolute_url())

    def test_goto_last_post_on_page(self):
        """last post on page redirect url is valid"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL - 1):
            post = testutils.reply_thread(self.thread)

        response = self.client.get(self.thread.get_last_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_URL % (self.thread.get_absolute_url(), post.pk)
        )

        response = self.client.get(response['location'])
        self.assertContains(response, post.get_absolute_url())


class GotoNewTests(GotoViewTestCase):
    def test_goto_first_post(self):
        """first unread post redirect url is valid"""
        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id)
        )

    def test_goto_first_new_post(self):
        """first unread post redirect url in already read thread is valid"""
        make_thread_read_aware(self.user, self.thread)
        read_thread(self.user, self.thread, self.thread.last_post)

        post = testutils.reply_thread(self.thread, posted_on=timezone.now())
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL - 1):
            testutils.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_URL % (self.thread.get_absolute_url(), post.pk)
        )

    def test_goto_first_new_post_on_next_page(self):
        """first unread post redirect url in already read multipage thread is valid"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL):
            testutils.reply_thread(self.thread, posted_on=timezone.now())

        make_thread_read_aware(self.user, self.thread)
        read_thread(self.user, self.thread, self.thread.last_post)

        post = testutils.reply_thread(self.thread, posted_on=timezone.now())
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL - 1):
            testutils.reply_thread(self.thread, posted_on=timezone.now())

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk)
        )

    def test_goto_first_new_post_in_read_thread(self):
        """goto new in read thread points to last post"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL):
            post = testutils.reply_thread(self.thread, posted_on=timezone.now())

        make_thread_read_aware(self.user, self.thread)
        read_thread(self.user, self.thread, self.thread.last_post)

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk)
        )

    def test_guest_goto_first_new_post_in_thread(self):
        """guest goto new in read thread points to last post"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL):
            post = testutils.reply_thread(self.thread, posted_on=timezone.now())

        self.logout_user()

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk)
        )


class GotoUnapprovedTests(GotoViewTestCase):
    def grant_permission(self):
        self.user.acl_cache['categories'][self.category.pk]['can_approve_content'] = 1
        override_acl(self.user, self.user.acl_cache)

    def test_view_validates_permission(self):
        """view validates permission to see unapproved posts"""
        response = self.client.get(self.thread.get_unapproved_post_url())
        self.assertContains(response, "You need permission to approve content", status_code=403)

        self.grant_permission()

        response = self.client.get(self.thread.get_unapproved_post_url())
        self.assertEqual(response.status_code, 302)

    def test_view_handles_no_unapproved_posts(self):
        """if thread has no unapproved posts, redirect to last post"""
        self.grant_permission()

        response = self.client.get(self.thread.get_unapproved_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            GOTO_URL % (self.thread.get_absolute_url(), self.thread.first_post_id)
        )

    def test_vie_handles_unapproved_posts(self):
        """if thread has unapproved posts, redirect to first of them"""
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL):
            testutils.reply_thread(self.thread, posted_on=timezone.now())

        make_thread_read_aware(self.user, self.thread)
        read_thread(self.user, self.thread, self.thread.last_post)

        post = testutils.reply_thread(self.thread, is_unapproved=True, posted_on=timezone.now())
        for _ in range(settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL - 1):
            testutils.reply_thread(self.thread, posted_on=timezone.now())

        self.grant_permission()

        response = self.client.get(self.thread.get_new_post_url())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'], GOTO_PAGE_URL % (self.thread.get_absolute_url(), 2, post.pk)
        )
