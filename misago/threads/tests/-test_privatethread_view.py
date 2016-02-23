from django.contrib.auth import get_user_model
from django.utils import timezone

from misago.acl.testutils import override_acl
from misago.categories.models import Category
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.models import ThreadParticipant


class PrivateThreadTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(PrivateThreadTests, self).setUp()

        self.category = Category.objects.private_threads()
        self.thread = testutils.post_thread(self.category)

    def test_anon_access_to_view(self):
        """anonymous user has no access to private thread"""
        self.logout_user()
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_non_participant_access_to_thread(self):
        """non-participant user has no access to private thread"""
        override_acl(self.user, {'can_use_private_threads': True})
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_owner_can_access_thread(self):
        """owner has access to private thread"""
        override_acl(self.user, {'can_use_private_threads': True})
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.thread.title, response.content)

    def test_participant_can_access_thread(self):
        """participant has access to private thread"""
        override_acl(self.user, {'can_use_private_threads': True})
        ThreadParticipant.objects.add_participant(self.thread, self.user)

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.thread.title, response.content)

    def test_removed_user_cant_access_thread(self):
        """removed user can't access thread"""
        override_acl(self.user, {'can_use_private_threads': True})

        ThreadParticipant.objects.add_participant(self.thread, self.user)
        ThreadParticipant.objects.remove_participant(self.thread, self.user)
        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_moderator_cant_access_unreported_thread(self):
        """moderator cant see private thread without reports"""
        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_moderator_can_access_reported_thread(self):
        """moderator can see private thread with reports"""
        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.thread.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.thread.title, response.content)

    def test_moderator_can_takeover_reported_thread(self):
        """moderator can take over private thread"""
        override_acl(self.user, {
            'can_use_private_threads': True,
            'can_moderate_private_threads': True
        })

        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'takeover'
        })
        self.assertEqual(response.status_code, 302)

        user = self.thread.threadparticipant_set.get(user=self.user)
        self.assertTrue(user.is_owner)

    def test_owner_can_pass_thread_to_participant(self):
        """thread owner can pass thread to other participant"""
        User = get_user_model()
        new_owner = User.objects.create_user("Bob", "bob@bob.com", "pass123")

        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participant(self.thread, new_owner)

        override_acl(self.user, {'can_use_private_threads': True})

        response = self.client.post(self.thread.get_absolute_url(), data={
            'thread_action': 'make_owner:%s' % new_owner.id
        })
        self.assertEqual(response.status_code, 302)

        user = self.thread.threadparticipant_set.get(user=self.user)
        self.assertFalse(user.is_owner)

        user = self.thread.threadparticipant_set.get(user=new_owner)
        self.assertTrue(user.is_owner)
