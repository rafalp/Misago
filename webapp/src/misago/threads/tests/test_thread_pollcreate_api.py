from django.urls import reverse

from ...acl.test import patch_user_acl
from ..models import Poll, Thread
from ..serializers.poll import MAX_POLL_OPTIONS
from ..test import patch_category_acl
from .test_thread_poll_api import ThreadPollApiTestCase


class ThreadPollCreateTests(ThreadPollApiTestCase):
    def test_anonymous(self):
        """api requires you to sign in to create poll"""
        self.logout_user()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_invalid_thread_id(self):
        """api validates that thread id is integer"""
        api_link = reverse(
            "misago:api:thread-poll-list", kwargs={"thread_pk": "kjha6dsa687sa"}
        )

        response = self.post(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_thread_id(self):
        """api validates that thread exists"""
        api_link = reverse(
            "misago:api:thread-poll-list", kwargs={"thread_pk": self.thread.pk + 1}
        )

        response = self.post(api_link)
        self.assertEqual(response.status_code, 404)

    @patch_user_acl({"can_start_polls": 0})
    def test_no_permission(self):
        """api validates that user has permission to start poll in thread"""
        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't start polls."})

    @patch_user_acl({"can_start_polls": 1})
    @patch_category_acl({"can_close_threads": False})
    def test_closed_thread_no_permission(self):
        """api validates that user has permission to start poll in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't start polls in it."},
        )

    @patch_user_acl({"can_start_polls": 1})
    @patch_category_acl({"can_close_threads": True})
    def test_closed_thread(self):
        """api validates that user has permission to start poll in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_user_acl({"can_start_polls": 1})
    @patch_category_acl({"can_close_threads": False})
    def test_closed_category_no_permission(self):
        """api validates that user has permission to start poll in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't start polls in it."},
        )

    @patch_user_acl({"can_start_polls": 1})
    @patch_category_acl({"can_close_threads": True})
    def test_closed_category(self):
        """api validates that user has permission to start poll in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_user_acl({"can_start_polls": 1})
    def test_other_user_thread_no_permission(self):
        """
        api validates that user has permission to start poll in other user's thread
        """
        self.thread.starter = None
        self.thread.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "You can't start polls in other users threads."}
        )

    @patch_user_acl({"can_start_polls": 2})
    def test_other_user_thread(self):
        """
        api validates that user has permission to start poll in other user's thread
        """
        self.thread.starter = None
        self.thread.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_no_permission_poll_exists(self):
        """api validates that user can't start second poll in thread"""
        self.thread.poll = Poll.objects.create(
            thread=self.thread,
            category=self.category,
            poster_name="Test",
            poster_slug="test",
            length=30,
            question="Test",
            choices=[{"hash": "t3st"}],
            allowed_choices=1,
        )

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "There's already a poll in this thread."}
        )

    def test_empty_data(self):
        """api handles empty request data"""
        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(len(response_json), 4)

    def test_length_validation(self):
        """api validates poll's length"""
        response = self.post(self.api_link, data={"length": -1})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["length"],
            ["Ensure this value is greater than or equal to 0."],
        )

        response = self.post(self.api_link, data={"length": 200})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["length"], ["Ensure this value is less than or equal to 180."]
        )

    def test_question_validation(self):
        """api validates question length"""
        response = self.post(self.api_link, data={"question": "abcd" * 255})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["question"],
            ["Ensure this field has no more than 255 characters."],
        )

    def test_validate_choice_length(self):
        """api validates single choice length"""
        response = self.post(
            self.api_link, data={"choices": [{"hash": "qwertyuiopas", "label": ""}]}
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["choices"], ["One or more poll choices are invalid."]
        )

        response = self.post(
            self.api_link,
            data={"choices": [{"hash": "qwertyuiopas", "label": "abcd" * 255}]},
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["choices"], ["One or more poll choices are invalid."]
        )

    def test_validate_two_choices(self):
        """api validates that there are at least two choices in poll"""
        response = self.post(self.api_link, data={"choices": [{"label": "Choice"}]})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["choices"],
            ["You need to add at least two choices to a poll."],
        )

    def test_validate_max_choices(self):
        """api validates that there are no more choices in poll than allowed number"""
        response = self.post(
            self.api_link,
            data={"choices": [{"label": "Choice"}] * (MAX_POLL_OPTIONS + 1)},
        )
        self.assertEqual(response.status_code, 400)

        error_formats = (MAX_POLL_OPTIONS, MAX_POLL_OPTIONS + 1)

        response_json = response.json()
        self.assertEqual(
            response_json["choices"],
            [
                "You can't add more than %s options to a single poll (added %s)."
                % error_formats
            ],
        )

    def test_allowed_choices_validation(self):
        """api validates allowed choices number"""
        response = self.post(self.api_link, data={"allowed_choices": 0})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["allowed_choices"],
            ["Ensure this value is greater than or equal to 1."],
        )

        response = self.post(
            self.api_link,
            data={
                "length": 0,
                "question": "Lorem ipsum",
                "allowed_choices": 3,
                "choices": [{"label": "Choice"}, {"label": "Choice"}],
            },
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["non_field_errors"],
            ["Number of allowed choices can't be greater than number of all choices."],
        )

    def test_poll_created(self):
        """api creates public poll if provided with valid data"""
        response = self.post(
            self.api_link,
            data={
                "length": 40,
                "question": "Select two best colors",
                "allowed_choices": 2,
                "allow_revotes": True,
                "is_public": True,
                "choices": [{"label": "\nRed "}, {"label": "Green"}, {"label": "Blue"}],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["poster_name"], self.user.username)
        self.assertEqual(response_json["length"], 40)
        self.assertEqual(response_json["question"], "Select two best colors")
        self.assertEqual(response_json["allowed_choices"], 2)
        self.assertTrue(response_json["allow_revotes"])
        self.assertEqual(response_json["votes"], 0)
        self.assertTrue(response_json["is_public"])

        self.assertEqual(len(response_json["choices"]), 3)
        self.assertEqual(len({c["hash"] for c in response_json["choices"]}), 3)
        self.assertEqual(
            [c["label"] for c in response_json["choices"]], ["Red", "Green", "Blue"]
        )

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertTrue(thread.has_poll)

        poll = thread.poll

        self.assertEqual(poll.category_id, self.category.id)
        self.assertEqual(poll.thread_id, self.thread.id)
        self.assertEqual(poll.poster_id, self.user.id)
        self.assertEqual(poll.poster_name, self.user.username)
        self.assertEqual(poll.poster_slug, self.user.slug)
        self.assertEqual(poll.length, 40)
        self.assertEqual(poll.question, "Select two best colors")
        self.assertEqual(poll.allowed_choices, 2)
        self.assertTrue(poll.allow_revotes)
        self.assertEqual(poll.votes, 0)
        self.assertTrue(poll.is_public)

        self.assertEqual(len(poll.choices), 3)
        self.assertEqual(len({c["hash"] for c in poll.choices}), 3)

        self.assertEqual(self.user.audittrail_set.count(), 1)
