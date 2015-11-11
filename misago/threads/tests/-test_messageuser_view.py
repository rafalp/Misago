import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import ThreadParticipant


class MessageUserTests(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
    field_name = ('misago.threads.posting.participants.'
                  'ThreadParticipantsFormMiddleware-users')

    def setUp(self):
        super(MessageUserTests, self).setUp()

        User = get_user_model()
        self.test_user = User.objects.create_user(
            "Bob", "bob@boberson.com", "Pass.123")

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
            reverse('misago:start_private_thread'),
            data={'submit': '1'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

    def test_cant_message_self(self):
        """user cant message himself"""
        self.override_acl(self.user)
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('btn-message', response.content)
        self.assertNotIn(reverse('misago:start_private_thread'),
                         response.content)

        self.override_acl(self.user)
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: self.user.username,
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual("You can't addres message to yourself.",
                         response_json['errors'][0])

    def test_cant_message_nobody(self):
        """user cant message nobody"""
        self.override_acl(self.user)
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: '',
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual("You have to specify message recipients.",
                         response_json['errors'][0])

    def test_cant_message_other_user(self):
        """cant message user that can't use private threads"""
        self.override_acl(self.user)
        self.override_acl(self.test_user, {'can_use_private_threads': False})

        response = self.client.get(self.test_user.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('btn-message', response.content)
        self.assertIn('participate in private threads.', response.content)
        self.assertNotIn(reverse('misago:start_private_thread'),
                         response.content)

        self.override_acl(self.user)
        self.override_acl(self.test_user, {'can_use_private_threads': False})
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: self.test_user.username,
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual("Bob can't participate in private threads.",
                         response_json['errors'][0])

    def test_cant_message_blocking_user(self):
        """cant message user that blocks us"""
        self.override_acl(self.user, {
            'can_add_everyone_to_private_threads': False
        })
        self.override_acl(self.test_user)

        self.test_user.blocks.add(self.user)

        response = self.client.get(self.test_user.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('btn-message', response.content)
        self.assertIn('Bob is blocking you.', response.content)
        self.assertNotIn(reverse('misago:start_private_thread'),
                         response.content)

        self.override_acl(self.user, {
            'can_add_everyone_to_private_threads': False
        })
        self.override_acl(self.test_user)
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: self.test_user.username,
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual("Bob is blocking you.",
                         response_json['errors'][0])

    def test_cant_message_nonexistant_users(self):
        """cant message users that don't exist"""
        self.override_acl(self.user)
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: 'hatsune, miku',
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual("One or more message recipients could "
                         "not be found: hatsune, miku",
                         response_json['errors'][0])

    def test_cant_message_too_many_users(self):
        """cant message too many users"""
        self.override_acl(self.user, {'max_private_thread_participants': 2})
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: 'hatsune, miku, yui',
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual("You can't start private thread "
                         "with more than than 2 users.",
                         response_json['errors'][0])

    def test_can_message_other_user(self):
        """can message other user"""
        self.override_acl(self.user)
        self.override_acl(self.test_user)

        response = self.client.get(self.test_user.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn('btn-message', response.content)
        self.assertIn(reverse('misago:start_private_thread'), response.content)

        self.override_acl(self.user)
        self.override_acl(self.test_user)
        response = self.client.post(
            reverse('misago:start_private_thread'),
            data={
                'title': 'Jingo Jango!',
                'post': 'Lorem ipsum dolor met.',
                self.field_name: self.test_user.username,
                'submit': '1',
            },
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        post_url = response_json['post_url']

        self.override_acl(self.user)
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Jingo Jango!', response.content)
        self.assertIn('Lorem ipsum dolor met.', response.content)

        thread = self.user.thread_set.order_by('-id').last()
        self.assertEqual(thread.title, 'Jingo Jango!')

        self.assertEqual(self.user,
                         thread.threadparticipant_set.get(is_owner=True).user)
        self.assertEqual(self.test_user,
                         thread.threadparticipant_set.get(is_owner=False).user)
