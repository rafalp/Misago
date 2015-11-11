import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread, ThreadParticipant


class ReplyPrivateThreadTests(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
    field_name = ('misago.threads.posting.participants.'
                  'ThreadParticipantsFormMiddleware-users')

    def setUp(self):
        super(ReplyPrivateThreadTests, self).setUp()

        User = get_user_model()
        self.test_user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

        self.override_acl(self.user)
        self.override_acl(self.test_user)

        self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Private Thread Test',
                'post': 'My name is ummm... Pat, I am new here.',
                self.field_name: self.test_user.username,
                'submit': '1',
            },
            **self.ajax_header)

        self.thread = Thread.objects.order_by('-id')[:1][0]

    def override_acl(self, user, acl=None):
        base_acl = {
            'can_use_private_threads': True,
            'can_start_private_threads': True
        }
        if acl:
            base_acl.update(acl)
        override_acl(user, base_acl)

    def test_empty_form_handling(self):
        """empty form isn't borking"""
        self.override_acl(self.user)
        response = self.client.post(
            self.thread.get_reply_api_url(),
            data={'submit': '1'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

    def test_reply_thread(self):
        """participant can reply private thread"""
        self.override_acl(self.user)
        self.override_acl(self.test_user)

        self.user.last_post_on = None
        self.user.save()

        response = self.client.post(
            self.thread.get_reply_api_url(),
            data={
                'post': 'Lorem ipsum dolor met.',
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        post_url = response_json['post_url']

        self.override_acl(self.user)
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('My name is ummm... Pat', response.content)
        self.assertIn('Lorem ipsum dolor met.', response.content)

    def test_cant_reply_abadoned_thread(self):
        """participant can't reply private thread with no other users"""
        self.override_acl(self.user)
        self.thread.threadparticipant_set.filter(user=self.test_user).delete()

        response = self.client.post(
            self.thread.get_reply_api_url(),
            data={
                'post': 'Lorem ipsum dolor met.',
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 403)

        response_json = json.loads(response.content)
        message = "You have to add new participants to thread before you will"
        self.assertTrue(response_json['message'].startswith(message))
