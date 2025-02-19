import json
from unittest.mock import patch

from .. import test
from ...acl.test import patch_user_acl
from ...users.test import create_test_user
from ..models import Thread, ThreadParticipant
from ..test import other_user_cant_use_private_threads
from .test_privatethreads import PrivateThreadsTestCase


class PrivateThreadPatchApiTestCase(PrivateThreadsTestCase):
    def setUp(self):
        super().setUp()

        self.thread = test.post_thread(self.category, poster=self.user)
        self.api_link = self.thread.get_api_url()

        self.other_user = create_test_user("Other_User", "otheruser@example.com")

    def patch(self, api_link, ops):
        return self.client.patch(
            api_link, json.dumps(ops), content_type="application/json"
        )


class PrivateThreadAddParticipantApiTests(PrivateThreadPatchApiTestCase):
    def test_add_participant_not_owner(self):
        """non-owner can't add participant"""
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.user.username}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": [
                    "You have to be thread owner to add new participants to it."
                ],
            },
        )

    def test_add_empty_username(self):
        """path validates username"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link, [{"op": "add", "path": "participants", "value": ""}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": ["You have to enter new participant's username."],
            },
        )

    def test_add_nonexistant_user(self):
        """can't user two times"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": "InvalidUser"}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["No user with this name exists."]},
        )

    def test_add_already_participant(self):
        """can't add user that is already participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.user.username}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": ["This user is already thread participant."],
            },
        )

    def test_add_blocking_user(self):
        """can't add user that is blocking us"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        self.other_user.blocks.add(self.user)

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.other_user.username}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["Other_User is blocking you."]},
        )

    @patch_user_acl(other_user_cant_use_private_threads)
    def test_add_no_perm_user(self):
        """can't add user that has no permission to use private threads"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.other_user.username}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": ["Other_User can't participate in private threads."],
            },
        )

    @patch_user_acl({"max_private_thread_participants": 3})
    def test_add_too_many_users(self):
        """can't add user that is already participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        for i in range(3):
            user = create_test_user("User%s" % i, "user%s@example.com" % i)
            ThreadParticipant.objects.add_participants(self.thread, [user])

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.other_user.username}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": ["You can't add any more new users to this thread."],
            },
        )

    def test_add_user_closed_thread(self):
        """adding user to closed thread fails for non-moderator"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.other_user.username}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": ["Only moderators can add participants to closed threads."],
            },
        )

    @patch("misago.threads.participants.notify_on_new_private_thread")
    def test_add_user(self, notify_on_new_private_thread_mock):
        """
        adding user to thread add user to thread as participant,
        sets event and notifies them
        """
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.other_user.username}],
        )

        # event was set on thread
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "added_participant")

        # notification about new private thread was triggered
        notify_on_new_private_thread_mock.delay.assert_called_once_with(
            self.user.id, self.thread.id, [self.other_user.id]
        )

    @patch_user_acl({"can_moderate_private_threads": True})
    @patch("misago.threads.participants.notify_on_new_private_thread")
    def test_add_user_to_other_user_thread_moderator(
        self, notify_on_new_private_thread_mock
    ):
        """moderators can add users to other users threads"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)

        self.thread.has_reported_posts = True
        self.thread.save()

        self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.user.username}],
        )

        # event was set on thread
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "entered_thread")

        # notification about new private thread was triggered
        notify_on_new_private_thread_mock.delay.assert_not_called()

    @patch_user_acl({"can_moderate_private_threads": True})
    @patch("misago.threads.participants.notify_on_new_private_thread")
    def test_add_user_to_closed_moderator(self, notify_on_new_private_thread_mock):
        """moderators can add users to closed threads"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        self.thread.is_closed = True
        self.thread.save()

        self.patch(
            self.api_link,
            [{"op": "add", "path": "participants", "value": self.other_user.username}],
        )

        # event was set on thread
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "added_participant")

        # notification about new private thread was triggered
        notify_on_new_private_thread_mock.delay.assert_called_once_with(
            self.user.id, self.thread.id, [self.other_user.id]
        )


class PrivateThreadRemoveParticipantApiTests(PrivateThreadPatchApiTestCase):
    def test_remove_empty(self):
        """api handles empty user id"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link, [{"op": "remove", "path": "participants", "value": ""}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["A valid integer is required."]},
        )

    def test_remove_invalid(self):
        """api validates user id type"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link, [{"op": "remove", "path": "participants", "value": "string"}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["A valid integer is required."]},
        )

    def test_remove_nonexistant(self):
        """removed user has to be participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.other_user.pk}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["Participant doesn't exist."]},
        )

    def test_remove_not_owner(self):
        """api validates if user trying to remove other user is an owner"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.other_user.pk}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": [
                    "You have to be thread owner to remove participants from it."
                ],
            },
        )

    def test_owner_remove_user_closed_thread(self):
        """api disallows owner to remove other user from closed thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.other_user.pk}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": [
                    "Only moderators can remove participants from closed threads."
                ],
            },
        )

    def test_user_leave_thread(self):
        """api allows user to remove themself from thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.user.pk}],
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["deleted"])

        # thread still exists
        self.assertTrue(Thread.objects.get(pk=self.thread.pk))

        # leave event has valid type
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "participant_left")

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertTrue(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(self.thread.participants.filter(pk=self.user.pk).count(), 0)

    def test_user_leave_closed_thread(self):
        """api allows user to remove themself from closed thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.user.pk}],
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["deleted"])

        # thread still exists
        self.assertTrue(Thread.objects.get(pk=self.thread.pk))

        # leave event has valid type
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "participant_left")

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertTrue(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(self.thread.participants.filter(pk=self.user.pk).count(), 0)

    @patch_user_acl({"can_moderate_private_threads": True})
    def test_moderator_remove_user(self):
        """api allows moderator to remove other user"""
        removed_user = create_test_user("RemovedUser", "removeduser@example.com")

        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(
            self.thread, [self.user, removed_user]
        )

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": removed_user.pk}],
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["deleted"])

        # thread still exists
        self.assertTrue(Thread.objects.get(pk=self.thread.pk))

        # leave event has valid type
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "participant_removed")

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertTrue(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        removed_user.refresh_from_db()
        self.assertTrue(removed_user.sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 2)
        self.assertEqual(self.thread.participants.filter(pk=removed_user.pk).count(), 0)

    def test_owner_remove_user(self):
        """api allows owner to remove other user"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.other_user.pk}],
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["deleted"])

        # thread still exists
        self.assertTrue(Thread.objects.get(pk=self.thread.pk))

        # leave event has valid type
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "participant_removed")

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertTrue(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(
            self.thread.participants.filter(pk=self.other_user.pk).count(), 0
        )

    def test_owner_leave_thread(self):
        """api allows owner to remove hisemf from thread, causing thread to close"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.user.pk}],
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["deleted"])

        # thread still exists and is closed
        self.assertTrue(Thread.objects.get(pk=self.thread.pk).is_closed)

        # leave event has valid type
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "owner_left")

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertTrue(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # user was removed from participation
        self.assertEqual(self.thread.participants.count(), 1)
        self.assertEqual(self.thread.participants.filter(pk=self.user.pk).count(), 0)

    def test_last_user_leave_thread(self):
        """api allows last user leave thread, causing thread to delete"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link,
            [{"op": "remove", "path": "participants", "value": self.user.pk}],
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["deleted"])

        # thread is gone
        with self.assertRaises(Thread.DoesNotExist):
            Thread.objects.get(pk=self.thread.pk)

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertTrue(self.user.sync_unread_private_threads)


class PrivateThreadTakeOverApiTests(PrivateThreadPatchApiTestCase):
    def test_empty_user_id(self):
        """api handles empty user id"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": ""}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["A valid integer is required."]},
        )

    def test_invalid_user_id(self):
        """api handles invalid user id"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": "dsadsa"}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["A valid integer is required."]},
        )

    def test_nonexistant_user_id(self):
        """api handles nonexistant user id"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "owner", "value": self.other_user.pk}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["Participant doesn't exist."]},
        )

    def test_no_permission(self):
        """non-moderator/owner can't change owner"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": self.user.pk}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": [
                    "Only thread owner and moderators can appoint a new thread owner."
                ],
            },
        )

    def test_no_change(self):
        """api validates that new owner id is same as current owner"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": self.user.pk}]
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"id": self.thread.pk, "detail": ["This user already is thread owner."]},
        )

    def test_change_closed_thread_owner(self):
        """non-moderator can't change owner in closed thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "owner", "value": self.other_user.pk}],
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "id": self.thread.pk,
                "detail": [
                    "Only moderators can appoint a new thread owner in a closed thread."
                ],
            },
        )

    def test_owner_change_thread_owner(self):
        """owner can pass thread ownership to other participant"""
        ThreadParticipant.objects.set_owner(self.thread, self.user)
        ThreadParticipant.objects.add_participants(self.thread, [self.other_user])

        response = self.patch(
            self.api_link,
            [{"op": "replace", "path": "owner", "value": self.other_user.pk}],
        )

        self.assertEqual(response.status_code, 200)

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertFalse(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # ownership was transfered
        self.assertEqual(self.thread.participants.count(), 2)
        self.assertTrue(ThreadParticipant.objects.get(user=self.other_user).is_owner)
        self.assertFalse(ThreadParticipant.objects.get(user=self.user).is_owner)

        # change was recorded in event
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "changed_owner")

    @patch_user_acl({"can_moderate_private_threads": True})
    def test_moderator_change_owner(self):
        """moderator can change thread owner to other user"""
        new_owner = create_test_user("NewOwner", "newowner@example.com")

        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user, new_owner])

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": new_owner.pk}]
        )

        self.assertEqual(response.status_code, 200)

        # valid users were flagged for sync
        new_owner.refresh_from_db()
        self.assertTrue(new_owner.sync_unread_private_threads)

        self.user.refresh_from_db()
        self.assertFalse(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # ownership was transferred
        self.assertEqual(self.thread.participants.count(), 3)
        self.assertTrue(ThreadParticipant.objects.get(user=new_owner).is_owner)
        self.assertFalse(ThreadParticipant.objects.get(user=self.user).is_owner)
        self.assertFalse(ThreadParticipant.objects.get(user=self.other_user).is_owner)

        # change was recorded in event
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "changed_owner")

    @patch_user_acl({"can_moderate_private_threads": True})
    def test_moderator_takeover(self):
        """moderator can takeover the thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": self.user.pk}]
        )

        self.assertEqual(response.status_code, 200)

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertFalse(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # ownership was transfered
        self.assertEqual(self.thread.participants.count(), 2)
        self.assertTrue(ThreadParticipant.objects.get(user=self.user).is_owner)
        self.assertFalse(ThreadParticipant.objects.get(user=self.other_user).is_owner)

        # change was recorded in event
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "tookover")

    @patch_user_acl({"can_moderate_private_threads": True})
    def test_moderator_closed_thread_takeover(self):
        """moderator can takeover closed thread thread"""
        ThreadParticipant.objects.set_owner(self.thread, self.other_user)
        ThreadParticipant.objects.add_participants(self.thread, [self.user])

        self.thread.is_closed = True
        self.thread.save()

        response = self.patch(
            self.api_link, [{"op": "replace", "path": "owner", "value": self.user.pk}]
        )

        self.assertEqual(response.status_code, 200)

        # valid users were flagged for sync
        self.user.refresh_from_db()
        self.assertFalse(self.user.sync_unread_private_threads)

        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.sync_unread_private_threads)

        # ownership was transferred
        self.assertEqual(self.thread.participants.count(), 2)
        self.assertTrue(ThreadParticipant.objects.get(user=self.user).is_owner)
        self.assertFalse(ThreadParticipant.objects.get(user=self.other_user).is_owner)

        # change was recorded in event
        event = self.thread.post_set.order_by("id").last()
        self.assertTrue(event.is_event)
        self.assertTrue(event.event_type, "tookover")
