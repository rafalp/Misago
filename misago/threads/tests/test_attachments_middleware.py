from rest_framework import serializers

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.conf import settings
from misago.threads import testutils
from misago.threads.api.postingendpoint import PostingEndpoint
from misago.threads.api.postingendpoint.attachments import (
    AttachmentsMiddleware, validate_attachments_count)
from misago.threads.models import Attachment, AttachmentType
from misago.users.testutils import AuthenticatedUserTestCase


class RequestMock(object):
    def __init__(self, data=None):
        self.data = data or {}


class AttachmentsMiddlewareTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(AttachmentsMiddlewareTests, self).setUp()

        self.category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category=self.category)
        self.post = self.thread.first_post

        self.post.update_fields = []

        self.override_acl()
        self.filetype = AttachmentType.objects.order_by('id').last()

    def override_acl(self, new_acl=None):
        override_acl(self.user, new_acl or {'max_attachment_size': 1024})

    def mock_attachment(self, user=True, post=None):
        return Attachment.objects.create(
            secret=Attachment.generate_new_secret(),
            filetype=self.filetype,
            post=post,
            size=1000,
            uploader=self.user if user else None,
            uploader_name=self.user.username,
            uploader_slug=self.user.slug,
            uploader_ip='127.0.0.1',
            filename='testfile_{}.zip'.format(Attachment.objects.count() + 1),
        )

    def test_use_this_middleware(self):
        """use_this_middleware returns False if we can't upload attachments"""
        middleware = AttachmentsMiddleware(user=self.user)

        self.override_acl({'max_attachment_size': 0})

        self.assertFalse(middleware.use_this_middleware())

        self.override_acl({'max_attachment_size': 1024})

        self.assertTrue(middleware.use_this_middleware())

    def test_middleware_is_optional(self):
        """middleware is optional"""
        INPUTS = [{}, {'attachments': []}]

        for test_input in INPUTS:
            middleware = AttachmentsMiddleware(
                request=RequestMock(test_input),
                mode=PostingEndpoint.START,
                user=self.user,
                post=self.post,
            )

            serializer = middleware.get_serializer()
            self.assertTrue(serializer.is_valid())

    def test_middleware_validates_ids(self):
        """middleware validates attachments ids"""
        INPUTS = ['none', ['a', 'b', 123], range(settings.MISAGO_POST_ATTACHMENTS_LIMIT + 1)]

        for test_input in INPUTS:
            middleware = AttachmentsMiddleware(
                request=RequestMock({
                    'attachments': test_input
                }),
                mode=PostingEndpoint.START,
                user=self.user,
                post=self.post,
            )

            serializer = middleware.get_serializer()
            self.assertFalse(serializer.is_valid(), "%r shouldn't validate" % test_input)

    def test_get_initial_attachments(self):
        """get_initial_attachments returns list of attachments already existing on post"""
        middleware = AttachmentsMiddleware(
            request=RequestMock(),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        )

        serializer = middleware.get_serializer()

        attachments = serializer.get_initial_attachments(
            middleware.mode, middleware.user, middleware.post
        )
        self.assertEqual(attachments, [])

        attachment = self.mock_attachment(post=self.post)
        attachments = serializer.get_initial_attachments(
            middleware.mode, middleware.user, middleware.post
        )
        self.assertEqual(attachments, [attachment])

    def test_get_new_attachments(self):
        """get_initial_attachments returns list of attachments already existing on post"""
        middleware = AttachmentsMiddleware(
            request=RequestMock(),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        )

        serializer = middleware.get_serializer()

        attachments = serializer.get_new_attachments(middleware.user, [1, 2, 3])
        self.assertEqual(attachments, [])

        attachment = self.mock_attachment()
        attachments = serializer.get_new_attachments(middleware.user, [attachment.pk])
        self.assertEqual(attachments, [attachment])

        # only own orphaned attachments may be assigned to posts
        other_user_attachment = self.mock_attachment(user=False)
        attachments = serializer.get_new_attachments(middleware.user, [other_user_attachment.pk])
        self.assertEqual(attachments, [])

    def test_cant_delete_attachment(self):
        """middleware validates if we have permission to delete other users attachments"""
        self.override_acl({
            'max_attachment_size': 1024,
            'can_delete_other_users_attachments': False,
        })

        attachment = self.mock_attachment(user=False, post=self.post)
        self.assertIsNone(attachment.uploader)

        serializer = AttachmentsMiddleware(
            request=RequestMock({
                'attachments': []
            }),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        ).get_serializer()

        self.assertFalse(serializer.is_valid())

    def test_add_attachments(self):
        """middleware adds attachments to post"""
        attachments = [
            self.mock_attachment(),
            self.mock_attachment(),
        ]

        middleware = AttachmentsMiddleware(
            request=RequestMock({
                'attachments': [a.pk for a in attachments]
            }),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        )

        serializer = middleware.get_serializer()
        self.assertTrue(serializer.is_valid())
        middleware.save(serializer)

        # attachments were associated with post
        self.assertEqual(self.post.update_fields, ['attachments_cache'])
        self.assertEqual(self.post.attachment_set.count(), 2)

        attachments_filenames = list(reversed([a.filename for a in attachments]))
        self.assertEqual([a['filename'] for a in self.post.attachments_cache],
                         attachments_filenames)

    def test_remove_attachments(self):
        """middleware removes attachment from post and db"""
        attachments = [
            self.mock_attachment(post=self.post),
            self.mock_attachment(post=self.post),
        ]

        middleware = AttachmentsMiddleware(
            request=RequestMock({
                'attachments': [attachments[0].pk]
            }),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        )

        serializer = middleware.get_serializer()
        self.assertTrue(serializer.is_valid())
        middleware.save(serializer)

        # attachments were associated with post
        self.assertEqual(self.post.update_fields, ['attachments_cache'])
        self.assertEqual(self.post.attachment_set.count(), 1)

        self.assertEqual(Attachment.objects.count(), 1)

        attachments_filenames = [attachments[0].filename]
        self.assertEqual([a['filename'] for a in self.post.attachments_cache],
                         attachments_filenames)

    def test_steal_attachments(self):
        """middleware validates if attachments are already assigned to other posts"""
        other_post = testutils.reply_thread(self.thread)

        attachments = [
            self.mock_attachment(post=other_post),
            self.mock_attachment(),
        ]

        middleware = AttachmentsMiddleware(
            request=RequestMock({
                'attachments': [attachments[0].pk, attachments[1].pk]
            }),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        )

        serializer = middleware.get_serializer()
        self.assertTrue(serializer.is_valid())
        middleware.save(serializer)

        # only unassociated attachment was associated with post
        self.assertEqual(self.post.update_fields, ['attachments_cache'])
        self.assertEqual(self.post.attachment_set.count(), 1)

        self.assertEqual(Attachment.objects.get(pk=attachments[0].pk).post, other_post)
        self.assertEqual(Attachment.objects.get(pk=attachments[1].pk).post, self.post)

    def test_edit_attachments(self):
        """middleware removes and adds attachments to post"""
        attachments = [
            self.mock_attachment(post=self.post),
            self.mock_attachment(post=self.post),
            self.mock_attachment(),
        ]

        middleware = AttachmentsMiddleware(
            request=RequestMock({
                'attachments': [attachments[0].pk, attachments[2].pk]
            }),
            mode=PostingEndpoint.EDIT,
            user=self.user,
            post=self.post,
        )

        serializer = middleware.get_serializer()
        self.assertTrue(serializer.is_valid())
        middleware.save(serializer)

        # attachments were associated with post
        self.assertEqual(self.post.update_fields, ['attachments_cache'])
        self.assertEqual(self.post.attachment_set.count(), 2)

        attachments_filenames = [attachments[2].filename, attachments[0].filename]
        self.assertEqual([a['filename'] for a in self.post.attachments_cache],
                         attachments_filenames)


class ValidateAttachmentsCountTests(AuthenticatedUserTestCase):
    def test_validate_attachments_count(self):
        """too large count of attachments is rejected"""
        validate_attachments_count(range(settings.MISAGO_POST_ATTACHMENTS_LIMIT))

        with self.assertRaises(serializers.ValidationError):
            validate_attachments_count(range(settings.MISAGO_POST_ATTACHMENTS_LIMIT + 1))
