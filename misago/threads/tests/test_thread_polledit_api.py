from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from ...acl.test import patch_user_acl
from ..serializers.poll import MAX_POLL_OPTIONS
from ..test import patch_category_acl
from .test_thread_poll_api import ThreadPollApiTestCase


class ThreadPollEditTests(ThreadPollApiTestCase):
    def setUp(self):
        super().setUp()

        self.mock_poll()

    def test_anonymous(self):
        """api requires you to sign in to edit poll"""
        self.logout_user()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)

    def test_invalid_thread_id(self):
        """api validates that thread id is integer"""
        api_link = reverse(
            "misago:api:thread-poll-detail",
            kwargs={"thread_pk": "kjha6dsa687sa", "pk": self.poll.pk},
        )

        response = self.put(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_thread_id(self):
        """api validates that thread exists"""
        api_link = reverse(
            "misago:api:thread-poll-detail",
            kwargs={"thread_pk": self.thread.pk + 1, "pk": self.poll.pk},
        )

        response = self.put(api_link)
        self.assertEqual(response.status_code, 404)

    def test_invalid_poll_id(self):
        """api validates that poll id is integer"""
        api_link = reverse(
            "misago:api:thread-poll-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": "sad98as7d97sa98"},
        )

        response = self.put(api_link)
        self.assertEqual(response.status_code, 404)

    def test_nonexistant_poll_id(self):
        """api validates that poll exists"""
        api_link = reverse(
            "misago:api:thread-poll-detail",
            kwargs={"thread_pk": self.thread.pk, "pk": self.poll.pk + 123},
        )

        response = self.put(api_link)
        self.assertEqual(response.status_code, 404)

    @patch_user_acl({"can_edit_polls": 0})
    def test_no_permission(self):
        """api validates that user has permission to edit poll in thread"""
        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "You can't edit polls."})

    @patch_user_acl({"can_edit_polls": 1, "poll_edit_time": 5})
    def test_no_permission_timeout(self):
        """api validates that user's window to edit poll in thread has closed"""
        self.poll.posted_on = timezone.now() - timedelta(minutes=15)
        self.poll.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't edit polls that are older than 5 minutes."},
        )

    @patch_user_acl({"can_edit_polls": 1})
    def test_no_permission_poll_closed(self):
        """api validates that user's window to edit poll in thread has closed"""
        self.poll.posted_on = timezone.now() - timedelta(days=15)
        self.poll.length = 5
        self.poll.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "This poll is over. You can't edit it."}
        )

    @patch_user_acl({"can_edit_polls": 1})
    def test_no_permission_other_user_poll(self):
        """api validates that user has permission to edit other user poll in thread"""
        self.poll.poster = None
        self.poll.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "You can't edit other users polls in this category."},
        )

    @patch_user_acl({"can_edit_polls": 1})
    @patch_category_acl({"can_close_threads": False})
    def test_no_permission_closed_thread(self):
        """api validates that user has permission to edit poll in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This thread is closed. You can't edit polls in it."},
        )

    @patch_user_acl({"can_edit_polls": 1})
    @patch_category_acl({"can_close_threads": True})
    def test_closed_thread(self):
        """api validates that user has permission to edit poll in closed thread"""
        self.thread.is_closed = True
        self.thread.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    @patch_user_acl({"can_edit_polls": 1})
    @patch_category_acl({"can_close_threads": False})
    def test_no_permission_closed_category(self):
        """api validates that user has permission to edit poll in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This category is closed. You can't edit polls in it."},
        )

    @patch_user_acl({"can_edit_polls": 1})
    @patch_category_acl({"can_close_threads": True})
    def test_closed_category(self):
        """api validates that user has permission to edit poll in closed category"""
        self.category.is_closed = True
        self.category.save()

        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_empty_data(self):
        """api handles empty request data"""
        response = self.put(self.api_link)
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(len(response_json), 4)

    def test_length_validation(self):
        """api validates poll's length"""
        response = self.put(self.api_link, data={"length": -1})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["length"],
            ["Ensure this value is greater than or equal to 0."],
        )

        response = self.put(self.api_link, data={"length": 200})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["length"], ["Ensure this value is less than or equal to 180."]
        )

    def test_question_validation(self):
        """api validates question length"""
        response = self.put(self.api_link, data={"question": "abcd" * 255})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["question"],
            ["Ensure this field has no more than 255 characters."],
        )

    def test_validate_choice_length(self):
        """api validates single choice length"""
        response = self.put(
            self.api_link, data={"choices": [{"hash": "qwertyuiopas", "label": ""}]}
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["choices"], ["One or more poll choices are invalid."]
        )

        response = self.put(
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
        response = self.put(self.api_link, data={"choices": [{"label": "Choice"}]})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["choices"],
            ["You need to add at least two choices to a poll."],
        )

    def test_validate_max_choices(self):
        """api validates that there are no more choices in poll than allowed number"""
        response = self.put(
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
        response = self.put(self.api_link, data={"allowed_choices": 0})
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(
            response_json["allowed_choices"],
            ["Ensure this value is greater than or equal to 1."],
        )

        response = self.put(
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

    def test_poll_all_choices_replaced(self):
        """api edits all poll choices out"""
        response = self.put(
            self.api_link,
            data={
                "length": 40,
                "question": "Select two best colors",
                "allowed_choices": 2,
                "allow_revotes": True,
                "is_public": True,
                "choices": [
                    {"label": "\nRed  "},
                    {"label": "Green"},
                    {"label": "Blue"},
                ],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["poster_name"], self.user.username)
        self.assertEqual(response_json["length"], 40)
        self.assertEqual(response_json["question"], "Select two best colors")
        self.assertEqual(response_json["allowed_choices"], 2)
        self.assertTrue(response_json["allow_revotes"])

        # you can't change poll's type after its posted
        self.assertFalse(response_json["is_public"])

        # choices were updated
        self.assertEqual(len(response_json["choices"]), 3)
        self.assertEqual(len({c["hash"] for c in response_json["choices"]}), 3)
        self.assertEqual(
            [c["label"] for c in response_json["choices"]], ["Red", "Green", "Blue"]
        )
        self.assertEqual([c["votes"] for c in response_json["choices"]], [0, 0, 0])
        self.assertEqual(
            [c["selected"] for c in response_json["choices"]], [False, False, False]
        )

        # votes were removed
        self.assertEqual(response_json["votes"], 0)
        self.assertEqual(self.poll.pollvote_set.count(), 0)

        self.assertEqual(self.user.audittrail_set.count(), 1)

    def test_poll_current_choices_edited(self):
        """api edits current poll choices"""
        response = self.put(
            self.api_link,
            data={
                "length": 40,
                "question": "Select two best colors",
                "allowed_choices": 2,
                "allow_revotes": True,
                "is_public": True,
                "choices": [
                    {"hash": "aaaaaaaaaaaa", "label": "\nFirst  ", "votes": 5555},
                    {"hash": "bbbbbbbbbbbb", "label": "Second", "votes": 5555},
                    {"hash": "gggggggggggg", "label": "Third", "votes": 5555},
                    {"hash": "dddddddddddd", "label": "Fourth", "votes": 5555},
                ],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["poster_name"], self.user.username)
        self.assertEqual(response_json["length"], 40)
        self.assertEqual(response_json["question"], "Select two best colors")
        self.assertEqual(response_json["allowed_choices"], 2)
        self.assertTrue(response_json["allow_revotes"])

        # you can't change poll's type after its posted
        self.assertFalse(response_json["is_public"])

        # choices were updated
        self.assertEqual(len(response_json["choices"]), 4)
        self.assertEqual(
            response_json["choices"],
            [
                {
                    "hash": "aaaaaaaaaaaa",
                    "label": "First",
                    "votes": 1,
                    "selected": False,
                },
                {
                    "hash": "bbbbbbbbbbbb",
                    "label": "Second",
                    "votes": 0,
                    "selected": False,
                },
                {
                    "hash": "gggggggggggg",
                    "label": "Third",
                    "votes": 2,
                    "selected": True,
                },
                {
                    "hash": "dddddddddddd",
                    "label": "Fourth",
                    "votes": 1,
                    "selected": True,
                },
            ],
        )

        # no votes were removed
        self.assertEqual(response_json["votes"], 4)
        self.assertEqual(self.poll.pollvote_set.count(), 4)

        self.assertEqual(self.user.audittrail_set.count(), 1)

    def test_poll_some_choices_edited(self):
        """api edits some poll choices"""
        response = self.put(
            self.api_link,
            data={
                "length": 40,
                "question": "Select two best colors",
                "allowed_choices": 2,
                "allow_revotes": True,
                "is_public": True,
                "choices": [
                    {"hash": "aaaaaaaaaaaa", "label": "\nFirst ", "votes": 5555},
                    {"hash": "bbbbbbbbbbbb", "label": "Second", "votes": 5555},
                    {"hash": "dsadsadsa788", "label": "New Option", "votes": 5555},
                ],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["poster_name"], self.user.username)
        self.assertEqual(response_json["length"], 40)
        self.assertEqual(response_json["question"], "Select two best colors")
        self.assertEqual(response_json["allowed_choices"], 2)
        self.assertTrue(response_json["allow_revotes"])

        # you can't change poll's type after its posted
        self.assertFalse(response_json["is_public"])

        # choices were updated
        self.assertEqual(len(response_json["choices"]), 3)
        self.assertEqual(
            response_json["choices"],
            [
                {
                    "hash": "aaaaaaaaaaaa",
                    "label": "First",
                    "votes": 1,
                    "selected": False,
                },
                {
                    "hash": "bbbbbbbbbbbb",
                    "label": "Second",
                    "votes": 0,
                    "selected": False,
                },
                {
                    "hash": response_json["choices"][2]["hash"],
                    "label": "New Option",
                    "votes": 0,
                    "selected": False,
                },
            ],
        )

        # no votes were removed
        self.assertEqual(response_json["votes"], 1)
        self.assertEqual(self.poll.pollvote_set.count(), 1)

        self.assertEqual(self.user.audittrail_set.count(), 1)

    @patch_user_acl({"can_edit_polls": 2, "poll_edit_time": 5})
    def test_moderate_user_poll(self):
        """api edits all poll choices out in other users poll, even if its over"""
        self.poll.poster = None
        self.poll.posted_on = timezone.now() - timedelta(days=15)
        self.poll.length = 5
        self.poll.save()

        response = self.put(
            self.api_link,
            data={
                "length": 40,
                "question": "Select two best colors",
                "allowed_choices": 2,
                "allow_revotes": True,
                "is_public": True,
                "choices": [
                    {"label": "\nRed  "},
                    {"label": "Green"},
                    {"label": "Blue"},
                ],
            },
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertEqual(response_json["poster_name"], self.user.username)
        self.assertEqual(response_json["length"], 40)
        self.assertEqual(response_json["question"], "Select two best colors")
        self.assertEqual(response_json["allowed_choices"], 2)
        self.assertTrue(response_json["allow_revotes"])

        # you can't change poll's type after its posted
        self.assertFalse(response_json["is_public"])

        # choices were updated
        self.assertEqual(len(response_json["choices"]), 3)
        self.assertEqual(len({c["hash"] for c in response_json["choices"]}), 3)
        self.assertEqual(
            [c["label"] for c in response_json["choices"]], ["Red", "Green", "Blue"]
        )
        self.assertEqual([c["votes"] for c in response_json["choices"]], [0, 0, 0])
        self.assertEqual(
            [c["selected"] for c in response_json["choices"]], [False, False, False]
        )

        # votes were removed
        self.assertEqual(response_json["votes"], 0)
        self.assertEqual(self.poll.pollvote_set.count(), 0)

        self.assertEqual(self.user.audittrail_set.count(), 1)
