from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from .. import testutils
from ..models import Post, Thread
from ..moderation import threads as threads_moderation
from ..moderation.posts import hide_post


class MockRequest(object):
    def __init__(self, user):
        self.user = user
        self.user_ip = '127.0.0.1'


class ThreadViewTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(ThreadViewTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)

    def override_acl(self, acl=None):
        category_acl = self.user.acl['categories'][self.category.pk]
        category_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_see_own_threads': 0,
            'can_hide_threads': 0,
            'can_approve_content': 0,
            'can_edit_posts': 0,
            'can_hide_posts': 0,
            'can_hide_own_posts': 0,
            'can_close_threads': 0,
            'post_edit_time': 0,
            'can_hide_events': 0,
        })

        if acl:
            category_acl.update(acl)

        override_acl(self.user, {
            'categories': {
                self.category.pk: category_acl
            }
        })


class ThreadVisibilityTests(ThreadViewTestCase):
    def test_thread_displays(self):
        """thread view has no showstoppers"""
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_shows_owner_thread(self):
        """view handles "owned threads only" """
        self.override_acl({
            'can_see_all_threads': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.thread.starter = self.user
        self.thread.save()

        self.override_acl({
            'can_see_all_threads': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_validates_category_permissions(self):
        """view validates category visiblity"""
        self.override_acl({
            'can_see': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.override_acl({
            'can_browse': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_view_shows_unapproved_thread(self):
        """view handles unapproved thread"""
        self.override_acl({
            'can_approve_content': 0
        })

        self.thread.is_unapproved = True
        self.thread.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        # grant permission to see unapproved content
        self.override_acl({
            'can_approve_content': 1
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

        # make test user thread's owner and remove permission to see unapproved
        # user should be able to see thread as its author anyway
        self.thread.starter = self.user
        self.thread.save()

        self.override_acl({
            'can_approve_content': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_shows_hidden_thread(self):
        """view handles hidden thread"""
        self.override_acl({
            'can_hide_threads': 0
        })

        self.thread.is_hidden = True
        self.thread.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        # threads owners are not extempt from hidden threads check
        self.thread.starter = self.user
        self.thread.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        # grant permission to see hidden content
        self.override_acl({
            'can_hide_threads': 1
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)


class ThreadPostsVisibilityTests(ThreadViewTestCase):
    def test_post_renders(self):
        """post renders"""
        post = testutils.reply_thread(self.thread, poster=self.user)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())

    def test_invalid_post_renders(self):
        """invalid post renders"""
        post = testutils.reply_thread(self.thread, poster=self.user)

        post.parsed = 'fiddled post content'
        post.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post's contents cannot be displayed.")
        self.assertNotContains(response, post.parsed)

    def test_hidden_post_visibility(self):
        """hidden post renders correctly"""
        post = testutils.reply_thread(self.thread, message="Hello, I'm hidden post!")
        hide_post(self.user, post)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is hidden. You cannot not see its contents.")
        self.assertNotContains(response, post.parsed)

        # posts authors are not extempt from seeing hidden posts content
        post.posted_by = self.user
        post.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is hidden. You cannot not see its contents.")
        self.assertNotContains(response, post.parsed)

        # permission to hide own posts isn't enought to see post content
        self.override_acl({
            'can_hide_own_posts': 1
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is hidden. You cannot not see its contents.")
        self.assertNotContains(response, post.parsed)

        # post's content is displayed after permission to see posts is granted
        self.override_acl({
            'can_hide_posts': 1
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is hidden. Only users with permission may see its contents.")
        self.assertNotContains(response, "This post is hidden. You cannot not see its contents.")
        self.assertContains(response, post.parsed)

    def test_unapproved_post_visibility(self):
        """unapproved post renders for its author and users with perm to approve content"""
        post = testutils.reply_thread(self.thread, is_unapproved=True)

        # post is hdden because we aren't its author nor user with permission to approve
        response = self.client.get(self.thread.get_absolute_url())
        self.assertNotContains(response, post.get_absolute_url())

        # post displays because we have permission to approve unapproved content
        self.override_acl({
            'can_approve_content': 1
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is unapproved.")
        self.assertContains(response, post.parsed)

        # post displays because we are its author
        post.poster = self.user
        post.save()

        self.override_acl({
            'can_approve_content': 0
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is unapproved.")
        self.assertContains(response, post.parsed)


class ThreadEventVisibilityTests(ThreadViewTestCase):
    def test_thread_events_render(self):
        """different thread events render"""
        TEST_ACTIONS = (
            (threads_moderation.pin_thread_globally, "Thread has been pinned globally."),
            (threads_moderation.pin_thread_locally, "Thread has been pinned locally."),
            (threads_moderation.unpin_thread, "Thread has been unpinned."),
            (threads_moderation.approve_thread, "Thread has been approved."),
            (threads_moderation.close_thread, "Thread has been closed."),
            (threads_moderation.open_thread, "Thread has been opened."),
            (threads_moderation.hide_thread, "Thread has been made hidden."),
            (threads_moderation.unhide_thread, "Thread has been revealed."),
        )

        self.thread.is_unapproved = True
        self.thread.save()

        for action, message in TEST_ACTIONS:
            self.override_acl({
                'can_approve_content': 1,
                'can_hide_threads': 1,
            })

            self.thread.post_set.filter(is_event=True).delete()
            action(MockRequest(self.user), self.thread)

            event = self.thread.post_set.filter(is_event=True)[0]

            # event renders
            response = self.client.get(self.thread.get_absolute_url())
            self.assertContains(response, event.get_absolute_url())
            self.assertContains(response, message)

            # hidden events don't render without permission
            hide_post(self.user, event)
            self.override_acl({
                'can_approve_content': 1,
                'can_hide_threads': 1,
            })

            response = self.client.get(self.thread.get_absolute_url())
            self.assertNotContains(response, event.get_absolute_url())
            self.assertNotContains(response, message)

            # hidden event renders with permission
            hide_post(self.user, event)
            self.override_acl({
                'can_approve_content': 1,
                'can_hide_threads': 1,
                'can_hide_events': 1,
            })

            response = self.client.get(self.thread.get_absolute_url())
            self.assertContains(response, event.get_absolute_url())
            self.assertContains(response, message)
            self.assertContains(response, "Hidden by")

    def test_changed_thread_title_event_renders(self):
        """changed thread title event renders"""
        threads_moderation.change_thread_title(MockRequest(self.user), self.thread, "Lorem renamed ipsum!")

        event = self.thread.post_set.filter(is_event=True)[0]
        self.assertEqual(event.event_type, 'changed_title')

        # event renders
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, event.get_absolute_url())
        self.assertContains(response, "title has been changed from")
        self.assertContains(response, self.thread.title)

    def test_thread_move_event_renders(self):
        """moved thread event renders"""
        self.thread.category = self.thread.category.parent
        self.thread.save()

        threads_moderation.move_thread(MockRequest(self.user), self.thread, self.category)

        event = self.thread.post_set.filter(is_event=True)[0]
        self.assertEqual(event.event_type, 'moved')

        # event renders
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, event.get_absolute_url())
        self.assertContains(response, "Thread has been moved from")

    def test_thread_merged_event_renders(self):
        """merged thread event renders"""
        other_thread = testutils.post_thread(category=self.category)
        threads_moderation.merge_thread(MockRequest(self.user), self.thread, other_thread)

        event = self.thread.post_set.filter(is_event=True)[0]
        self.assertEqual(event.event_type, 'merged')

        # event renders
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, event.get_absolute_url())
        self.assertContains(response, "thread has been merged into this thread")


class ThreadAttachmentsViewTests(ThreadViewTestCase):
    def mock_attachment_cache(self, data):
        json = {
            'url': {},
            'size': 16914,
            'filename': 'Archiwum.zip',
            'filetype': 'ZIP',
            'is_image': False,
            'uploaded_on': '2016-10-22T21:17:40.408710Z',
            'uploader_name': 'BobBoberson'
        }

        json.update(data)
        return json

    def test_attachments_display(self):
        """thread posts show list of attachments below them"""
        post = self.thread.first_post

        post.attachments_cache = [
            self.mock_attachment_cache({
                'url': {
                    'index': '/attachment/loremipsum-123/',
                    'thumb': None,
                    'uploader': '/user/bobboberson-123/'
                },
                'filename': 'Archiwum-1.zip',
            }),
            self.mock_attachment_cache({
                'url': {
                    'index': '/attachment/loremipsum-223/',
                    'thumb': '/attachment/thumb/loremipsum-223/',
                    'uploader': '/user/bobboberson-223/'
                },
                'is_image': True,
                'filename': 'Archiwum-2.zip'
            }),
            self.mock_attachment_cache({
                'url': {
                    'index': '/attachment/loremipsum-323/',
                    'thumb': None,
                    'uploader': '/user/bobboberson-323/'
                },
                'filename': 'Archiwum-3.zip'
            })
        ]
        post.save()

        # attachments render
        response = self.client.get(self.thread.get_absolute_url())

        for attachment in post.attachments_cache:
            self.assertContains(response, attachment['filename'])
            self.assertContains(response, attachment['uploader_name'])
            self.assertContains(response, attachment['url']['index'])
            self.assertContains(response, attachment['url']['uploader'])

            if attachment['url']['thumb']:
                self.assertContains(response, attachment['url']['thumb'])
