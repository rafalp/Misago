from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from ...acl.test import patch_user_acl
from ..models import Poll
from ..test import patch_category_acl
from .test_thread_poll_api import ThreadPollApiTestCase

User = get_user_model()


class ThreadGetVotesTests(ThreadPollApiTestCase):
    def setUp(self):
        super().setUp()

        self.mock_poll()

        self.poll.is_public = True
        self.poll.save()

        self.api_link = reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": self.thread.pk, "pk": self.poll.pk},
        )

    def test_anonymous(self):
        """api allows guests to get poll votes"""
        self.logout_user()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

    def test_invalid_thread_id(self):
        """api validates that thread id is integer"""
        api_link = reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": "kjha6dsa687sa", "pk": self.poll.pk},
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_thread_id(self):
        """api validates that thread exists"""
        api_link = reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": self.thread.pk + 1, "pk": self.poll.pk},
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)

    def test_invalid_poll_id(self):
        """api validates that poll id is integer"""
        api_link = reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": self.thread.pk, "pk": "sad98as7d97sa98"},
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_poll_id(self):
        """api validates that poll exists"""
        api_link = reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": self.thread.pk, "pk": self.poll.pk + 123},
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)

    @patch_user_acl({"can_always_see_poll_voters": False})
    def test_no_permission(self):
        """api chcecks permission to see poll voters"""
        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_nonpublic_poll(self):
        """api validates that poll is public"""
        self.logout_user()

        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_get_votes(self):
        """api returns list of voters"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 4)

        self.assertEqual(
            [c["label"] for c in response_json], ["Alpha", "Beta", "Gamma", "Delta"]
        )
        self.assertEqual([c["votes"] for c in response_json], [1, 0, 2, 1])
        self.assertEqual([len(c["voters"]) for c in response_json], [1, 0, 2, 1])

        self.assertEqual(
            [[v["username"] for v in c["voters"]] for c in response_json][0][0], "User"
        )

        user = User.objects.get(slug="user")

        self.assertEqual(
            [[v["url"] for v in c["voters"]] for c in response_json][0][0],
            user.get_absolute_url(),
        )

    @patch_user_acl({"can_always_see_poll_voters": True})
    def test_get_votes_private_poll(self):
        """api returns list of voters on private poll for user with permission"""
        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 4)

        self.assertEqual(
            [c["label"] for c in response_json], ["Alpha", "Beta", "Gamma", "Delta"]
        )
        self.assertEqual([c["votes"] for c in response_json], [1, 0, 2, 1])
        self.assertEqual([len(c["voters"]) for c in response_json], [1, 0, 2, 1])

        self.assertEqual(
            [[v["username"] for v in c["voters"]] for c in response_json][0][0], "User"
        )

        user = User.objects.get(slug="user")

        self.assertEqual(
            [[v["url"] for v in c["voters"]] for c in response_json][0][0],
            user.get_absolute_url(),
        )


class ThreadPostVotesTests(ThreadPollApiTestCase):
    def setUp(self):
        super().setUp()

        self.mock_poll()

        self.api_link = reverse(
            "misago:api:thread-poll-votes",
            kwargs={"thread_pk": self.thread.pk, "pk": self.poll.pk},
        )

    def delete_user_votes(self):
        self.poll.choices[2]["votes"] = 1
        self.poll.choices[3]["votes"] = 0
        self.poll.votes = 2
        self.poll.save()

        self.poll.pollvote_set.filter(voter=self.user).delete()

    def test_anonymous(self):
        """api requires you to sign in to vote in poll"""
        self.logout_user()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_empty_vote_json(self):
        """api validates if vote that user has made was empty"""
        self.delete_user_votes()

        response = self.client.post(
            self.api_link, "[]", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "You have to make a choice."})

    def test_empty_vote_form(self):
        """api validates if vote that user has made was empty"""
        self.delete_user_votes()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "You have to make a choice."})

    def test_malformed_vote(self):
        """api validates if vote that user has made was correctly structured"""
        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "dict".'}
        )

        response = self.post(self.api_link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "dict".'}
        )

        response = self.post(self.api_link, data="hello")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "str".'}
        )

        response = self.post(self.api_link, data=123)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "int".'}
        )

    def test_invalid_choices(self):
        """api validates if vote that user has made overlaps with allowed votes"""
        self.delete_user_votes()

        response = self.post(self.api_link, data=["lorem", "ipsum"])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "One or more of poll choices were invalid."}
        )

    def test_too_many_choices(self):
        """api validates if vote that user has made overlaps with allowed votes"""
        self.poll.allowed_choices = 1
        self.poll.allow_revotes = True
        self.poll.save()

        response = self.post(self.api_link, data=["aaaaaaaaaaaa", "bbbbbbbbbbbb"])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "This poll disallows voting for more than 1 choice."},
        )

    def test_revote(self):
        """
        api validates if user is trying to change vote in poll that disallows revoting
        """
        response = self.post(self.api_link, data=["lorem", "ipsum"])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You have already voted in this poll."}
        )

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "dict".'}
        )

    @patch_category_acl({"can_close_threads": False})
    def test_vote_in_closed_thread_no_permission(self):
        """api validates is user has permission to vote poll in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This thread is closed. You can't vote in it."}
        )

    @patch_category_acl({"can_close_threads": True})
    def test_vote_in_closed_thread(self):
        """api validates is user has permission to vote poll in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_category_acl({"can_close_threads": False})
    def test_vote_in_closed_category_no_permission(self):
        """api validates is user has permission to vote poll in closed category"""
        self.category.is_closed = True
        self.category.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't vote in it."},
        )

    @patch_category_acl({"can_close_threads": True})
    def test_vote_in_closed_category(self):
        """api validates is user has permission to vote poll in closed category"""
        self.category.is_closed = True
        self.category.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_vote_in_finished_poll(self):
        """api valdiates if poll has finished before letting user to vote in it"""
        self.poll.posted_on = timezone.now() - timedelta(days=15)
        self.poll.length = 5
        self.poll.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This poll is over. You can't vote in it."}
        )

        self.poll.length = 50
        self.poll.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": 'Expected a list of items but got type "dict".'}
        )

    def test_fresh_vote(self):
        """api handles first vote in poll"""
        self.delete_user_votes()

        response = self.post(self.api_link, data=["aaaaaaaaaaaa", "bbbbbbbbbbbb"])
        self.assertEqual(response.status_code, 200)

        # validate state change
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.votes, 4)
        self.assertEqual([c["votes"] for c in poll.choices], [2, 1, 1, 0])

        for choice in poll.choices:
            self.assertNotIn("selected", choice)

        self.assertEqual(poll.pollvote_set.count(), 4)

        # validate response json
        response_json = response.json()
        self.assertEqual(response_json["votes"], 4)
        self.assertEqual([c["votes"] for c in response_json["choices"]], [2, 1, 1, 0])
        self.assertEqual(
            [c["selected"] for c in response_json["choices"]],
            [True, True, False, False],
        )

        self.assertFalse(response_json["acl"]["can_vote"])

    def test_vote_change(self):
        """api handles vote change"""
        self.poll.allow_revotes = True
        self.poll.save()

        response = self.post(self.api_link, data=["aaaaaaaaaaaa", "bbbbbbbbbbbb"])
        self.assertEqual(response.status_code, 200)

        # validate state change
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.votes, 4)
        self.assertEqual([c["votes"] for c in poll.choices], [2, 1, 1, 0])

        for choice in poll.choices:
            self.assertNotIn("selected", choice)

        self.assertEqual(poll.pollvote_set.count(), 4)

        # validate response json
        response_json = response.json()
        self.assertEqual(response_json["votes"], 4)
        self.assertEqual([c["votes"] for c in response_json["choices"]], [2, 1, 1, 0])
        self.assertEqual(
            [c["selected"] for c in response_json["choices"]],
            [True, True, False, False],
        )

        self.assertTrue(response_json["acl"]["can_vote"])
