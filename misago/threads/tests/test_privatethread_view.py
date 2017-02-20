from misago.acl.testutils import override_acl
from misago.threads import testutils
from misago.threads.models import ThreadParticipant

from .test_privatethreads import PrivateThreadsTestCase


class PrivateThreadViewTests(PrivateThreadsTestCase):
    def setUp(self):
        super(PrivateThreadViewTests, self).setUp()

        self.thread = testutils.post_thread(self.category, poster=self.user)
        self.test_link = self.thread.get_absolute_url()

    def test_anonymous(self):
        """anonymous user can't see private thread"""
        self.logout_user()

        response = self.client.get(self.test_link)
        self.assertContains(response, "sign in to use private threads", status_code=403)

    def test_no_permission(self):
        """user needs to have permission to see private thread"""
        override_acl(self.user, {'can_use_private_threads': 0})

        response = self.client.get(self.test_link)
        self.assertContains(response, "t use private threads", status_code=403)

    def test_no_participant(self):
        """user cant see thread he isn't part of"""
        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 404)

    def test_mod_not_reported(self):
        """moderator can't see private thread that has no reports"""
        override_acl(self.user, {'can_moderate_private_threads': 1})

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 404)

    def test_reported_not_mod(self):
        """non-mod can't see private thread that has reported posts"""
        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 404)

    def test_can_see_owner(self):
        """user can see thread he is owner of"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.client.get(self.test_link)
        self.assertContains(response, self.thread.title)

    def test_can_see_participant(self):
        """user can see thread he is participant of"""
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.client.get(self.test_link)
        self.assertContains(response, self.thread.title)

    def test_mod_can_see_reported(self):
        """moderator can see private thread that has reports"""
        override_acl(self.user, {'can_moderate_private_threads': 1})

        self.thread.has_reported_posts = True
        self.thread.save()

        response = self.client.get(self.test_link)
        self.assertContains(response, self.thread.title)
