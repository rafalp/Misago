import os

from django.urls import reverse

from misago.acl import add_acl
from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.threads import testutils
from misago.threads.models import Attachment
from misago.threads.serializers import AttachmentSerializer
from misago.users.testutils import AuthenticatedUserTestCase


TESTFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfiles')
TEST_DOCUMENT_PATH = os.path.join(TESTFILES_DIR, 'document.pdf')


class EditorApiTestCase(AuthenticatedUserTestCase):
    def setUp(self):
        super(EditorApiTestCase, self).setUp()

        self.category = Category.objects.get(slug='first-category')

    def override_acl(self, acl=None):
        final_acl = self.user.acl_cache['categories'][self.category.pk]
        final_acl.update({
            'can_see': 1,
            'can_browse': 1,
            'can_see_all_threads': 1,
            'can_start_threads': 0,
            'can_reply_threads': 0,
            'can_edit_threads': 0,
            'can_edit_posts': 0,
            'can_hide_own_threads': 0,
            'can_hide_own_posts': 0,
            'thread_edit_time': 0,
            'post_edit_time': 0,
            'can_hide_threads': 0,
            'can_hide_posts': 0,
            'can_protect_posts': 0,
            'can_move_posts': 0,
            'can_merge_posts': 0,
            'can_pin_threads': 0,
            'can_close_threads': 0,
            'can_move_threads': 0,
            'can_merge_threads': 0,
            'can_approve_content': 0,
            'can_report_content': 0,
            'can_see_reports': 0,
            'can_see_posts_likes': 0,
            'can_like_posts': 0,
            'can_hide_events': 0,
        })

        if acl:
            final_acl.update(acl)

        browseable_categories = []
        if final_acl['can_browse']:
            browseable_categories.append(self.category.pk)

        override_acl(
            self.user, {
                'browseable_categories': browseable_categories,
                'categories': {
                    self.category.pk: final_acl,
                },
            }
        )


class ThreadPostEditorApiTests(EditorApiTestCase):
    def setUp(self):
        super(ThreadPostEditorApiTests, self).setUp()

        self.api_link = reverse('misago:api:thread-editor')

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertContains(response, "You need to be signed in", status_code=403)

    def test_category_visibility_validation(self):
        """endpoint omits non-browseable categories"""
        self.override_acl({'can_browse': 0})

        response = self.client.get(self.api_link)
        self.assertContains(response, "No categories that allow new threads", status_code=403)

    def test_category_disallowing_new_threads(self):
        """endpoint omits category disallowing starting threads"""
        self.override_acl({'can_start_threads': 0})

        response = self.client.get(self.api_link)
        self.assertContains(response, "No categories that allow new threads", status_code=403)

    def test_category_closed_disallowing_new_threads(self):
        """endpoint omits closed category"""
        self.override_acl({'can_start_threads': 2, 'can_close_threads': 0})

        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertContains(response, "No categories that allow new threads", status_code=403)

    def test_category_closed_allowing_new_threads(self):
        """endpoint adds closed category that allows new threads"""
        self.override_acl({'can_start_threads': 2, 'can_close_threads': 1})

        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': True,
                    'hide': False,
                    'pin': 0,
                },
            }
        )

    def test_category_allowing_new_threads(self):
        """endpoint adds category that allows new threads"""
        self.override_acl({'can_start_threads': 2})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': False,
                    'hide': False,
                    'pin': 0,
                },
            }
        )

    def test_category_allowing_closing_threads(self):
        """endpoint adds category that allows new closed threads"""
        self.override_acl({'can_start_threads': 2, 'can_close_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': True,
                    'hide': False,
                    'pin': 0,
                },
            }
        )

    def test_category_allowing_locally_pinned_threads(self):
        """endpoint adds category that allows locally pinned threads"""
        self.override_acl({'can_start_threads': 2, 'can_pin_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': False,
                    'hide': False,
                    'pin': 1,
                },
            }
        )

    def test_category_allowing_globally_pinned_threads(self):
        """endpoint adds category that allows globally pinned threads"""
        self.override_acl({'can_start_threads': 2, 'can_pin_threads': 2})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': False,
                    'hide': False,
                    'pin': 2,
                },
            }
        )

    def test_category_allowing_hidden_threads(self):
        """endpoint adds category that allows globally pinned threads"""
        self.override_acl({'can_start_threads': 2, 'can_hide_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': 0,
                    'hide': 1,
                    'pin': 0,
                },
            }
        )

        self.override_acl({'can_start_threads': 2, 'can_hide_threads': 2})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(
            response_json[0], {
                'id': self.category.pk,
                'name': self.category.name,
                'level': 0,
                'post': {
                    'close': False,
                    'hide': True,
                    'pin': 0,
                },
            }
        )


class ThreadReplyEditorApiTests(EditorApiTestCase):
    def setUp(self):
        super(ThreadReplyEditorApiTests, self).setUp()

        self.thread = testutils.post_thread(category=self.category)
        self.api_link = reverse(
            'misago:api:thread-post-editor', kwargs={
                'thread_pk': self.thread.pk,
            }
        )

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertContains(response, "You have to sign in to reply threads.", status_code=403)

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        self.override_acl({'can_see': 0})
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_browse': 0})
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_see_all_threads': 0})
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_no_reply_permission(self):
        """permssion to reply is validated"""
        self.override_acl({'can_reply_threads': 0})

        response = self.client.get(self.api_link)
        self.assertContains(
            response, "You can't reply to threads in this category.", status_code=403
        )

    def test_closed_category(self):
        """permssion to reply in closed category is validated"""
        self.override_acl({'can_reply_threads': 1, 'can_close_threads': 0})

        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertContains(
            response,
            "This category is closed. You can't reply to threads in it.",
            status_code=403
        )

        # allow to post in closed category
        self.override_acl({'can_reply_threads': 1, 'can_close_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_closed_thread(self):
        """permssion to reply in closed thread is validated"""
        self.override_acl({'can_reply_threads': 1, 'can_close_threads': 0})

        self.thread.is_closed = True
        self.thread.save()

        response = self.client.get(self.api_link)
        self.assertContains(
            response, "You can't reply to closed threads in this category.", status_code=403
        )

        # allow to post in closed thread
        self.override_acl({'can_reply_threads': 1, 'can_close_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_allow_reply_thread(self):
        """api returns 200 code if thread reply is allowed"""
        self.override_acl({'can_reply_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_reply_to_visibility(self):
        """api validates replied post visibility"""
        self.override_acl({'can_reply_threads': 1})

        # unapproved reply can't be replied to
        unapproved_reply = testutils.reply_thread(
            self.thread,
            is_unapproved=True,
        )

        response = self.client.get('{}?reply={}'.format(self.api_link, unapproved_reply.pk))
        self.assertEqual(response.status_code, 404)

        # hidden reply can't be replied to
        self.override_acl({'can_reply_threads': 1})

        hidden_reply = testutils.reply_thread(self.thread, is_hidden=True)

        response = self.client.get('{}?reply={}'.format(self.api_link, hidden_reply.pk))
        self.assertContains(response, "You can't reply to hidden posts", status_code=403)

    def test_reply_to_other_thread_post(self):
        """api validates is replied post belongs to same thread"""
        other_thread = testutils.post_thread(category=self.category)
        reply_to = testutils.reply_thread(other_thread)

        response = self.client.get('{}?reply={}'.format(self.api_link, reply_to.pk))
        self.assertEqual(response.status_code, 404)

    def test_reply_to_event(self):
        """events can't be edited"""
        self.override_acl({'can_reply_threads': 1})

        reply_to = testutils.reply_thread(self.thread, is_event=True)

        response = self.client.get('{}?reply={}'.format(self.api_link, reply_to.pk))

        self.assertContains(response, "You can't reply to events.", status_code=403)

    def test_reply_to(self):
        """api includes replied to post details in response"""
        self.override_acl({'can_reply_threads': 1})

        reply_to = testutils.reply_thread(self.thread)

        response = self.client.get('{}?reply={}'.format(self.api_link, reply_to.pk))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'id': reply_to.pk,
                'post': reply_to.original,
                'poster': reply_to.poster_name,
            }
        )


class EditReplyEditorApiTests(EditorApiTestCase):
    def setUp(self):
        super(EditReplyEditorApiTests, self).setUp()

        self.thread = testutils.post_thread(category=self.category)
        self.post = testutils.reply_thread(self.thread, poster=self.user)

        self.api_link = reverse(
            'misago:api:thread-post-editor',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.post.pk,
            }
        )

    def test_anonymous_user_request(self):
        """endpoint validates if user is authenticated"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertContains(response, "You have to sign in to edit posts.", status_code=403)

    def test_thread_visibility(self):
        """thread's visibility is validated"""
        self.override_acl({'can_see': 0})
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_browse': 0})
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

        self.override_acl({'can_see_all_threads': 0})
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

    def test_no_edit_permission(self):
        """permssion to edit is validated"""
        self.override_acl({'can_edit_posts': 0})

        response = self.client.get(self.api_link)
        self.assertContains(response, "You can't edit posts in this category.", status_code=403)

    def test_closed_category(self):
        """permssion to edit in closed category is validated"""
        self.override_acl({'can_edit_posts': 1, 'can_close_threads': 0})

        self.category.is_closed = True
        self.category.save()

        response = self.client.get(self.api_link)
        self.assertContains(
            response, "This category is closed. You can't edit posts in it.", status_code=403
        )

        # allow to edit in closed category
        self.override_acl({'can_edit_posts': 1, 'can_close_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_closed_thread(self):
        """permssion to edit in closed thread is validated"""
        self.override_acl({'can_edit_posts': 1, 'can_close_threads': 0})

        self.thread.is_closed = True
        self.thread.save()

        response = self.client.get(self.api_link)
        self.assertContains(
            response, "This thread is closed. You can't edit posts in it.", status_code=403
        )

        # allow to edit in closed thread
        self.override_acl({'can_edit_posts': 1, 'can_close_threads': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_protected_post(self):
        """permssion to edit protected post is validated"""
        self.override_acl({'can_edit_posts': 1, 'can_protect_posts': 0})

        self.post.is_protected = True
        self.post.save()

        response = self.client.get(self.api_link)
        self.assertContains(
            response, "This post is protected. You can't edit it.", status_code=403
        )

        # allow to post in closed thread
        self.override_acl({'can_edit_posts': 1, 'can_protect_posts': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_post_visibility(self):
        """edited posts visibility is validated"""
        self.override_acl({'can_edit_posts': 1})

        self.post.is_hidden = True
        self.post.save()

        response = self.client.get(self.api_link)
        self.assertContains(response, "This post is hidden, you can't edit it.", status_code=403)

        # allow hidden edition
        self.override_acl({'can_edit_posts': 1, 'can_hide_posts': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        # test unapproved post
        self.post.is_hidden = False
        self.post.poster = None
        self.post.save()

        self.override_acl({'can_edit_posts': 2, 'can_approve_content': 0})

        self.post.is_unapproved = True
        self.post.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 404)

        # allow unapproved edition
        self.override_acl({'can_edit_posts': 2, 'can_approve_content': 1})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_post_is_event(self):
        """events can't be edited"""
        self.override_acl()

        self.post.is_event = True
        self.post.save()

        response = self.client.get(self.api_link)

        self.assertContains(response, "Events can't be edited.", status_code=403)

    def test_other_user_post(self):
        """api validates if other user's post can be edited"""
        self.override_acl({'can_edit_posts': 1})

        self.post.poster = None
        self.post.save()

        response = self.client.get(self.api_link)
        self.assertContains(
            response, "You can't edit other users posts in this category.", status_code=403
        )

        # allow other users post edition
        self.override_acl({'can_edit_posts': 2})

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_edit_first_post_hidden(self):
        """endpoint returns valid configuration for editor of hidden thread's first post"""
        self.override_acl({'can_hide_threads': 1, 'can_edit_posts': 2})

        self.thread.is_hidden = True
        self.thread.save()
        self.thread.first_post.is_hidden = True
        self.thread.first_post.save()

        api_link = reverse(
            'misago:api:thread-post-editor',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.thread.first_post.pk,
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        """endpoint returns valid configuration for editor"""
        for _ in range(3):
            self.override_acl({'max_attachment_size': 1000})

            with open(TEST_DOCUMENT_PATH, 'rb') as upload:
                response = self.client.post(
                    reverse('misago:api:attachment-list'), data={
                        'upload': upload,
                    }
                )
            self.assertEqual(response.status_code, 200)

        attachments = list(Attachment.objects.order_by('id'))

        attachments[0].uploader = None
        attachments[0].save()

        for attachment in attachments[:2]:
            attachment.post = self.post
            attachment.save()

        self.override_acl({'can_edit_posts': 1})
        response = self.client.get(self.api_link)

        for attachment in attachments:
            add_acl(self.user, attachment)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {
                'id': self.post.pk,
                'api': self.post.get_api_url(),
                'post': self.post.original,
                'can_protect': False,
                'is_protected': self.post.is_protected,
                'poster': self.post.poster_name,
                'attachments': [
                    AttachmentSerializer(attachments[1], context={'user': self.user}).data,
                    AttachmentSerializer(attachments[0], context={'user': self.user}).data,
                ],
            }
        )
