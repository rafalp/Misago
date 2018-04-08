from django.urls import reverse

from misago.acl import add_acl
from misago.core.utils import serialize_datetime
from misago.threads.models import Poll, Thread
from misago.threads.serializers.poll import MAX_POLL_OPTIONS

from .test_thread_poll_api import ThreadPollApiTestCase


class ThreadPollCreateTests(ThreadPollApiTestCase):
    def test_anonymous(self):
        """api requires you to sign in to create poll"""
        self.logout_user()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This action is not available to guests.",
        })

    def test_invalid_thread_id(self):
        """api validates that thread id is integer"""
        api_link = reverse(
            'misago:api:thread-poll-list', kwargs={
                'thread_pk': 'kjha6dsa687sa',
            }
        )

        response = self.post(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': "NOT FOUND",
        })

    def test_nonexistant_thread_id(self):
        """api validates that thread exists"""
        api_link = reverse(
            'misago:api:thread-poll-list', kwargs={
                'thread_pk': self.thread.pk + 1,
            }
        )

        response = self.post(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': "No Thread matches the given query.",
        })

    def test_no_permission(self):
        """api validates that user has permission to start poll in thread"""
        self.override_acl({'can_start_polls': 0})

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't start polls.",
        })

    def test_no_permission_closed_thread(self):
        """api validates that user has permission to start poll in closed thread"""
        self.override_acl(category={'can_close_threads': 0})

        self.thread.is_closed = True
        self.thread.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This thread is closed. You can't start polls in it.",
        })

        self.override_acl(category={'can_close_threads': 1})

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_no_permission_closed_category(self):
        """api validates that user has permission to start poll in closed category"""
        self.override_acl(category={'can_close_threads': 0})

        self.category.is_closed = True
        self.category.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This category is closed. You can't start polls in it.",
        })

        self.override_acl(category={'can_close_threads': 1})

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_no_permission_other_user_thread(self):
        """api validates that user has permission to start poll in other user's thread"""
        self.override_acl({'can_start_polls': 1})

        self.thread.starter = None
        self.thread.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You can't start polls in other users threads.",
        })

        self.override_acl({'can_start_polls': 2})

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_no_permission_poll_exists(self):
        """api validates that user can't start second poll in thread"""
        self.thread.poll = Poll.objects.create(
            thread=self.thread,
            category=self.category,
            poster_name='Test',
            poster_slug='test',
            poster_ip='127.0.0.1',
            length=30,
            question='Test',
            choices=[
                {
                    'hash': 't3st'
                },
            ],
            allowed_choices=1,
        )

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "There's already a poll in this thread.",
        })

    def test_empty_data(self):
        """api handles empty request data"""
        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["This field is required."],
            'length': ["This field is required."],
            'allowed_choices': ["This field is required."],
        })

    def test_length_validation(self):
        """api validates poll's length"""
        response = self.post(
            self.api_link, data={
                'length': -1,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["This field is required."],
            'length': ["Ensure this value is greater than or equal to 0."],
            'allowed_choices': ["This field is required."],
        })

        response = self.post(
            self.api_link, data={
                'length': 200,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["This field is required."],
            'length': ["Ensure this value is less than or equal to 180."],
            'allowed_choices': ["This field is required."],
        })

    def test_question_validation(self):
        """api validates question length"""
        response = self.post(
            self.api_link, data={
                'question': 'abcd' * 255,
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["Ensure this field has no more than 255 characters."],
            'choices': ["This field is required."],
            'length': ["This field is required."],
            'allowed_choices': ["This field is required."],
        })

    def test_validate_choice_length(self):
        """api validates single choice length"""
        response = self.post(
            self.api_link, data={
                'choices': [
                    {
                        'hash': 'qwertyuiopas',
                        'label': '',
                    },
                ],
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["One or more poll choices are invalid."],
            'length': ["This field is required."],
            'allowed_choices': ["This field is required."],
        })

        response = self.post(
            self.api_link,
            data={
                'choices': [
                    {
                        'hash': 'qwertyuiopas',
                        'label': 'abcd' * 255,
                    },
                ],
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["One or more poll choices are invalid."],
            'length': ["This field is required."],
            'allowed_choices': ["This field is required."],
        })

    def test_validate_two_choices(self):
        """api validates that there are at least two choices in poll"""
        response = self.post(self.api_link, data={'choices': [{'label': 'Choice'}]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["You need to add at least two choices to a poll."],
            'length': ["This field is required."],
            'allowed_choices': ["This field is required."],
        })

    def test_validate_max_choices(self):
        """api validates that there are no more choices in poll than allowed number"""
        response = self.post(
            self.api_link, data={
                'choices': [
                    {
                        'label': 'Choice',
                    },
                ] * (MAX_POLL_OPTIONS + 1),
            }
        )
        self.assertEqual(response.status_code, 400)

        error_formats = (MAX_POLL_OPTIONS, MAX_POLL_OPTIONS + 1)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': [
                "You can't add more than %s options to a single poll (added %s)." % error_formats
            ],
            'length': ["This field is required."],
            'allowed_choices': ["This field is required."],
        })

    def test_allowed_choices_validation(self):
        """api validates allowed choices number"""
        response = self.post(self.api_link, data={'allowed_choices': 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'question': ["This field is required."],
            'choices': ["This field is required."],
            'length': ["This field is required."],
            'allowed_choices': ["Ensure this value is greater than or equal to 1."],
        })

        response = self.post(
            self.api_link,
            data={
                'length': 0,
                'question': "Lorem ipsum",
                'allowed_choices': 3,
                'choices': [
                    {
                        'label': 'Choice',
                    },
                    {
                        'label': 'Choice',
                    },
                ],
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': [
                "Number of allowed choices can't be greater than number of all choices."
            ],
        })

    def test_poll_created(self):
        """api creates public poll if provided with valid data"""
        response = self.post(
            self.api_link,
            data={
                'length': 40,
                'question': "Select two best colors",
                'allowed_choices': 2,
                'allow_revotes': True,
                'is_public': True,
                'choices': [
                    {
                        'label': '\nRed ',
                    },
                    {
                        'label': 'Green',
                    },
                    {
                        'label': 'Blue',
                    },
                ],
            }
        )
        self.assertEqual(response.status_code, 200)
        self.maxDiff = None

        poll = Poll.objects.all()[0]
        add_acl(self.user, poll)

        expected_choices = []
        for choice in poll.choices:
            expected_choices.append(choice.copy())
            expected_choices[-1]['selected'] = False

        self.assertEqual(response.json(), {
            'id': poll.id,
            'poster_name': self.user.username,
            'posted_on': serialize_datetime(poll.posted_on),
            'length': 40,
            'question': "Select two best colors",
            'allowed_choices': 2,
            'allow_revotes': True,
            'votes': 0,
            'is_public': True,
            'acl': poll.acl,
            'choices': expected_choices,
            'api': {
                'index': poll.get_api_url(),
                'votes': poll.get_votes_api_url(),
            },
            'url': {
                'poster': self.user.get_absolute_url(),
            },
        })
        
        self.assertEqual(len(poll.choices), 3)
        self.assertEqual(len(set([c['hash'] for c in poll.choices])), 3)
        self.assertEqual([c['label'] for c in poll.choices], ['Red', 'Green', 'Blue'])

        thread = Thread.objects.get(pk=self.thread.pk)
        self.assertTrue(thread.has_poll)
        self.assertEqual(thread.poll, poll)
