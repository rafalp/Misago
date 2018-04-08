from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase


class UserSignatureTests(AuthenticatedUserTestCase):
    """tests for user signature RPC (POST to /api/users/1/signature/)"""

    def setUp(self):
        super(UserSignatureTests, self).setUp()
        self.link = '/api/users/%s/signature/' % self.user.pk

    def test_signature_no_permission(self):
        """edit signature api with no ACL returns 403"""
        override_acl(self.user, {
            'can_have_signature': 0,
        })

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You don't have permission to change signature.",
        })

    def test_signature_locked(self):
        """locked edit signature returns 403"""
        override_acl(self.user, {
            'can_have_signature': 1,
        })

        self.user.is_signature_locked = True
        self.user.signature_lock_user_message = 'Your siggy is banned.'
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "Your signature is locked. You can't change it.",
            'extra': "<p>Your siggy is banned.</p>",
        })

    def test_get_signature(self):
        """GET to api returns json with no signature"""
        override_acl(self.user, {
            'can_have_signature': 1,
        })

        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'signature': None,
            'limit': 256,
        })

    def test_post_empty_signature(self):
        """empty POST empties user signature"""
        override_acl(self.user, {
            'can_have_signature': 1,
        })

        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.post(
            self.link,
            data={
                'signature': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'signature': None,
            'limit': 256,
        })

    def test_post_too_long_signature(self):
        """too long new signature errors"""
        override_acl(self.user, {
            'can_have_signature': 1,
        })

        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.post(
            self.link,
            data={
                'signature': 'abcd' * 1000,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Signature is too long."],
        })

    def test_post_good_signature(self):
        """POST with good signature changes user signature"""
        override_acl(self.user, {
            'can_have_signature': 1,
        })

        self.user.is_signature_locked = False
        self.user.save()

        response = self.client.post(
            self.link,
            data={
                'signature': 'Hello, **bros**!',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'signature': {
                'html': '<p>Hello, <strong>bros</strong>!</p>',
                'plain': 'Hello, **bros**!',
            },
            'limit': 256,
        })

        # API updates user in database
        self.reload_user()
        self.assertEqual(self.user.signature_parsed, '<p>Hello, <strong>bros</strong>!</p>')
