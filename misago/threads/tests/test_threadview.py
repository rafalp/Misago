# -*- coding: utf-8 -*-
from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.conf import settings
from misago.threads import testutils
from misago.threads.checksums import update_post_checksum
from misago.threads.events import record_event
from misago.threads.moderation import threads as threads_moderation
from misago.threads.moderation import hide_post
from misago.users.testutils import AuthenticatedUserTestCase


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
        category_acl = self.user.acl_cache['categories'][self.category.pk]
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
                self.category.pk: category_acl,
            },
        })


class ThreadVisibilityTests(ThreadViewTestCase):
    def test_thread_displays(self):
        """thread view has no showstoppers"""
        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_shows_owner_thread(self):
        """view handles "owned threads" only"""
        self.override_acl({'can_see_all_threads': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.thread.starter = self.user
        self.thread.save()

        self.override_acl({'can_see_all_threads': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_validates_category_permissions(self):
        """view validates category visiblity"""
        self.override_acl({'can_see': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_browse': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_view_shows_unapproved_thread(self):
        """view handles unapproved thread"""
        self.override_acl({'can_approve_content': 0})

        self.thread.is_unapproved = True
        self.thread.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        # grant permission to see unapproved content
        self.override_acl({'can_approve_content': 1})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

        # make test user thread's owner and remove permission to see unapproved
        # user should be able to see thread as its author anyway
        self.thread.starter = self.user
        self.thread.save()

        self.override_acl({'can_approve_content': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, self.thread.title)

    def test_view_shows_hidden_thread(self):
        """view handles hidden thread"""
        self.override_acl({'can_hide_threads': 0})

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
        self.override_acl({'can_hide_threads': 1})

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
        self.override_acl({'can_hide_own_posts': 1})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is hidden. You cannot not see its contents.")
        self.assertNotContains(response, post.parsed)

        # post's content is displayed after permission to see posts is granted
        self.override_acl({'can_hide_posts': 1})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(
            response, "This post is hidden. Only users with permission may see its contents."
        )
        self.assertNotContains(response, "This post is hidden. You cannot not see its contents.")
        self.assertContains(response, post.parsed)

    def test_unapproved_post_visibility(self):
        """unapproved post renders for its author and users with perm to approve content"""
        post = testutils.reply_thread(self.thread, is_unapproved=True)

        # post is hdden because we aren't its author nor user with permission to approve
        response = self.client.get(self.thread.get_absolute_url())
        self.assertNotContains(response, post.get_absolute_url())

        # post displays because we have permission to approve unapproved content
        self.override_acl({'can_approve_content': 1})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is unapproved.")
        self.assertContains(response, post.parsed)

        # post displays because we are its author
        post.poster = self.user
        post.save()

        self.override_acl({'can_approve_content': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertContains(response, "This post is unapproved.")
        self.assertContains(response, post.parsed)


class ThreadEventVisibilityTests(ThreadViewTestCase):
    def test_thread_events_render(self):
        """different thread events render"""
        TEST_ACTIONS = [
            (threads_moderation.pin_thread_globally, "Thread has been pinned globally."),
            (threads_moderation.pin_thread_locally, "Thread has been pinned locally."),
            (threads_moderation.unpin_thread, "Thread has been unpinned."),
            (threads_moderation.approve_thread, "Thread has been approved."),
            (threads_moderation.close_thread, "Thread has been closed."),
            (threads_moderation.open_thread, "Thread has been opened."),
            (threads_moderation.hide_thread, "Thread has been made hidden."),
            (threads_moderation.unhide_thread, "Thread has been revealed."),
        ]

        self.thread.is_unapproved = True
        self.thread.save()

        for action, message in TEST_ACTIONS:
            self.override_acl({'can_approve_content': 1, 'can_hide_threads': 1})

            self.thread.post_set.filter(is_event=True).delete()
            action(MockRequest(self.user), self.thread)

            event = self.thread.post_set.filter(is_event=True)[0]

            # event renders
            response = self.client.get(self.thread.get_absolute_url())
            self.assertContains(response, event.get_absolute_url())
            self.assertContains(response, message)

            # hidden events don't render without permission
            hide_post(self.user, event)
            self.override_acl({'can_approve_content': 1, 'can_hide_threads': 1})

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

            # Event is only loaded if thread has events flag
            self.thread.has_events = False
            self.thread.save()

            self.override_acl({
                'can_approve_content': 1,
                'can_hide_threads': 1,
                'can_hide_events': 1,
            })

            response = self.client.get(self.thread.get_absolute_url())
            self.assertNotContains(response, event.get_absolute_url())

    def test_events_limit(self):
        """forum will trim oldest events if theres more than allowed by config"""
        events_limit = settings.MISAGO_EVENTS_PER_PAGE
        events = []

        for _ in range(events_limit + 5):
            event = record_event(MockRequest(self.user), self.thread, 'closed')
            events.append(event)

        # test that only events within limits were rendered
        response = self.client.get(self.thread.get_absolute_url())

        for event in events[5:]:
            self.assertContains(response, event.get_absolute_url())
        for event in events[:5]:
            self.assertNotContains(response, event.get_absolute_url())

    def test_events_dont_take_space(self):
        """events dont take space away from posts"""
        posts_limit = settings.MISAGO_POSTS_PER_PAGE
        events_limit = settings.MISAGO_EVENTS_PER_PAGE
        events = []

        for _ in range(events_limit + 5):
            event = record_event(MockRequest(self.user), self.thread, 'closed')
            events.append(event)

        posts = []
        for _ in range(posts_limit - 1):
            post = testutils.reply_thread(self.thread)
            posts.append(post)

        # test that all events and posts within limits were rendered
        response = self.client.get(self.thread.get_absolute_url())

        for event in events[5:]:
            self.assertContains(response, event.get_absolute_url())
        for post in posts:
            self.assertContains(response, post.get_absolute_url())

        # add second page to thread with more events
        for _ in range(posts_limit):
            post = testutils.reply_thread(self.thread)
        for _ in range(events_limit):
            event = record_event(MockRequest(self.user), self.thread, 'closed')
            events.append(event)

        # see first page
        response = self.client.get(self.thread.get_absolute_url())

        for event in events[5:events_limit]:
            self.assertContains(response, event.get_absolute_url())
        for post in posts[:posts_limit - 1]:
            self.assertContains(response, post.get_absolute_url())

        # see second page
        response = self.client.get('%s2/' % self.thread.get_absolute_url())
        for event in events[5 + events_limit:]:
            self.assertContains(response, event.get_absolute_url())
        for post in posts[posts_limit - 1:]:
            self.assertContains(response, post.get_absolute_url())

    def test_changed_thread_title_event_renders(self):
        """changed thread title event renders"""
        threads_moderation.change_thread_title(
            MockRequest(self.user), self.thread, "Lorem renamed ipsum!"
        )

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
            'uploader_name': 'BobBoberson',
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
                    'uploader': '/user/bobboberson-123/',
                },
                'filename': 'Archiwum-1.zip',
            }),
            self.mock_attachment_cache({
                'url': {
                    'index': '/attachment/loremipsum-223/',
                    'thumb': '/attachment/thumb/loremipsum-223/',
                    'uploader': '/user/bobboberson-223/',
                },
                'is_image': True,
                'filename': 'Archiwum-2.zip',
            }),
            self.mock_attachment_cache({
                'url': {
                    'index': '/attachment/loremipsum-323/',
                    'thumb': None,
                    'uploader': '/user/bobboberson-323/',
                },
                'filename': 'Archiwum-3.zip',
            }),
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


class ThreadPollViewTests(ThreadViewTestCase):
    def test_poll_voted_display(self):
        """view has no showstoppers when displaying voted poll"""
        poll = testutils.post_poll(self.thread, self.user)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, poll.question)
        self.assertContains(response, '4 votes')
        self.assertNotContains(response, 'Save your vote')

    def test_poll_unvoted_display(self):
        """view has no showstoppers when displaying poll vote form"""
        poll = testutils.post_poll(self.thread, self.user)
        poll.pollvote_set.all().delete()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, poll.question)
        self.assertContains(response, 'Save your vote')

    def test_poll_anonymous_view(self):
        """view has no showstoppers when displaying poll to anon user"""
        poll = testutils.post_poll(self.thread, self.user)

        self.logout_user()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, poll.question)
        self.assertContains(response, '4 votes')
        self.assertNotContains(response, 'Save your vote')


class ThreadLikedPostsViewTests(ThreadViewTestCase):
    def test_liked_posts_display(self):
        """view has no showstoppers on displaying posts with likes"""
        testutils.like_post(self.thread.first_post, self.user)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, '"is_liked": true')

    def test_liked_posts_no_permission(self):
        """
        view has no showstoppers on displaying posts with likes without perm
        """
        testutils.like_post(self.thread.first_post, self.user)

        self.override_acl({'can_see_posts_likes': 0})

        response = self.client.get(self.thread.get_absolute_url())
        self.assertNotContains(response, '"is_liked": true')
        self.assertNotContains(response, '"is_liked": false')
        self.assertContains(response, '"is_liked": null')


class ThreadAnonViewTests(ThreadViewTestCase):
    def test_anonymous_user_view_no_showstoppers_display(self):
        """kitchensink thread view has no showstoppers for anons"""
        poll = testutils.post_poll(self.thread, self.user)
        event = record_event(MockRequest(self.user), self.thread, 'closed')

        hidden_event = record_event(MockRequest(self.user), self.thread, 'opened')
        hide_post(self.user, hidden_event)

        unapproved_post = testutils.reply_thread(self.thread, is_unapproved=True)
        post = testutils.reply_thread(self.thread)

        self.logout_user()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertContains(response, poll.question)
        self.assertContains(response, event.get_absolute_url())
        self.assertContains(response, post.get_absolute_url())
        self.assertNotContains(response, hidden_event.get_absolute_url())
        self.assertNotContains(response, unapproved_post.get_absolute_url())


class ThreadUnicodeSupportTests(ThreadViewTestCase):
    def test_category_name(self):
        """unicode in category name causes no showstopper"""
        self.category.name = u'Łódź'
        self.category.slug = 'Lodz'

        self.category.save()

        self.override_acl()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_thread_title(self):
        """unicode in thread title causes no showstopper"""
        self.thread.title = u'Łódź'
        self.thread.slug = 'Lodz'

        self.thread.save()

        self.override_acl()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_post_content(self):
        """unicode in thread title causes no showstopper"""
        self.thread.first_post.original = u'Łódź'
        self.thread.first_post.parsed = u'<p>Łódź</p>'

        update_post_checksum(self.thread.first_post)

        self.thread.first_post.save()

        self.override_acl()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_user_rank(self):
        """unicode in user rank causes no showstopper"""
        self.user.title = u'Łódź'
        self.user.rank.name = u'Łódź'
        self.user.rank.title = u'Łódź'

        self.user.rank.save()
        self.user.save()

        self.override_acl()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
