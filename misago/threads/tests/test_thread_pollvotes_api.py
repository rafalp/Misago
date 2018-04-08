from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from misago.acl import add_acl
from misago.core.utils import serialize_datetime
from misago.threads.models import Poll

from .test_thread_poll_api import ThreadPollApiTestCase


UserModel = get_user_model()


class ThreadGetVotesTests(ThreadPollApiTestCase):
    def setUp(self):
        super(ThreadGetVotesTests, self).setUp()

        self.mock_poll()

        self.poll.is_public = True
        self.poll.save()

        self.api_link = reverse(
            'misago:api:thread-poll-votes',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.poll.pk,
            }
        )

    def get_votes_json(self):
        choices_votes = {choice['hash']: [] for choice in self.poll.choices}
        queryset = self.poll.pollvote_set.order_by('-id').select_related()
        for vote in queryset:
            if vote.voter:
                url = vote.voter.get_absolute_url()
            else:
                url = None

            choices_votes[vote.choice_hash].append({
                'username': vote.voter_name,
                'voted_on': serialize_datetime(vote.voted_on),
                'url': url
            })
        return choices_votes

    def test_anonymous(self):
        """api allows guests to get poll votes"""
        self.logout_user()

        votes_json = self.get_votes_json()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'hash': 'aaaaaaaaaaaa',
                'label': 'Alpha',
                'votes': 1,
                'voters': votes_json['aaaaaaaaaaaa'],
            },
            {
                'hash': 'bbbbbbbbbbbb',
                'label': 'Beta',
                'votes': 0,
                'voters': [],
            },
            {
                'hash': 'gggggggggggg',
                'label': 'Gamma',
                'votes': 2,
                'voters': votes_json['gggggggggggg'],
            },
            {
                'hash': 'dddddddddddd',
                'label': 'Delta',
                'votes': 1,
                'voters': votes_json['dddddddddddd'],
            },
        ])

        self.assertEqual(len(votes_json['aaaaaaaaaaaa']), 1)
        self.assertEqual(len(votes_json['bbbbbbbbbbbb']), 0)
        self.assertEqual(len(votes_json['gggggggggggg']), 2)
        self.assertEqual(len(votes_json['dddddddddddd']), 1)

    def test_invalid_thread_id(self):
        """api validates that thread id is integer"""
        api_link = reverse(
            'misago:api:thread-poll-votes',
            kwargs={
                'thread_pk': 'kjha6dsa687sa',
                'pk': self.poll.pk,
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': "NOT FOUND",
        })

    def test_nonexistant_thread_id(self):
        """api validates that thread exists"""
        api_link = reverse(
            'misago:api:thread-poll-votes',
            kwargs={
                'thread_pk': self.thread.pk + 1,
                'pk': self.poll.pk,
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': "No Thread matches the given query.",
        })

    def test_invalid_poll_id(self):
        """api validates that poll id is integer"""
        api_link = reverse(
            'misago:api:thread-poll-votes',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': 'sad98as7d97sa98',
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': "NOT FOUND",
        })

    def test_nonexistant_poll_id(self):
        """api validates that poll exists"""
        api_link = reverse(
            'misago:api:thread-poll-votes',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.poll.pk + 123,
            }
        )

        response = self.client.get(api_link)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': "NOT FOUND",
        })

    def test_no_permission(self):
        """api chcecks permission to see poll voters"""
        self.override_acl({'can_always_see_poll_voters': False})

        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You dont have permission to this poll's voters.",
        })

    def test_nonpublic_poll(self):
        """api validates that poll is public"""
        self.logout_user()

        self.poll.is_public = False
        self.poll.save()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You dont have permission to this poll's voters.",
        })

    def test_get_votes(self):
        """api returns list of voters"""
        votes_json = self.get_votes_json()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'hash': 'aaaaaaaaaaaa',
                'label': 'Alpha',
                'votes': 1,
                'voters': votes_json['aaaaaaaaaaaa'],
            },
            {
                'hash': 'bbbbbbbbbbbb',
                'label': 'Beta',
                'votes': 0,
                'voters': [],
            },
            {
                'hash': 'gggggggggggg',
                'label': 'Gamma',
                'votes': 2,
                'voters': votes_json['gggggggggggg'],
            },
            {
                'hash': 'dddddddddddd',
                'label': 'Delta',
                'votes': 1,
                'voters': votes_json['dddddddddddd'],
            },
        ])

        self.assertEqual(len(votes_json['aaaaaaaaaaaa']), 1)
        self.assertEqual(len(votes_json['bbbbbbbbbbbb']), 0)
        self.assertEqual(len(votes_json['gggggggggggg']), 2)
        self.assertEqual(len(votes_json['dddddddddddd']), 1)

    def test_get_votes_private_poll(self):
        """api returns list of voters on private poll for user with permission"""
        self.override_acl({'can_always_see_poll_voters': True})

        self.poll.is_public = False
        self.poll.save()

        votes_json = self.get_votes_json()

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                'hash': 'aaaaaaaaaaaa',
                'label': 'Alpha',
                'votes': 1,
                'voters': votes_json['aaaaaaaaaaaa'],
            },
            {
                'hash': 'bbbbbbbbbbbb',
                'label': 'Beta',
                'votes': 0,
                'voters': [],
            },
            {
                'hash': 'gggggggggggg',
                'label': 'Gamma',
                'votes': 2,
                'voters': votes_json['gggggggggggg'],
            },
            {
                'hash': 'dddddddddddd',
                'label': 'Delta',
                'votes': 1,
                'voters': votes_json['dddddddddddd'],
            },
        ])

        self.assertEqual(len(votes_json['aaaaaaaaaaaa']), 1)
        self.assertEqual(len(votes_json['bbbbbbbbbbbb']), 0)
        self.assertEqual(len(votes_json['gggggggggggg']), 2)
        self.assertEqual(len(votes_json['dddddddddddd']), 1)


class ThreadPostVotesTests(ThreadPollApiTestCase):
    def setUp(self):
        super(ThreadPostVotesTests, self).setUp()

        self.mock_poll()

        self.api_link = reverse(
            'misago:api:thread-poll-votes',
            kwargs={
                'thread_pk': self.thread.pk,
                'pk': self.poll.pk,
            }
        )

    def delete_user_votes(self):
        self.poll.choices[2]['votes'] = 1
        self.poll.choices[3]['votes'] = 0
        self.poll.votes = 2
        self.poll.save()

        self.poll.pollvote_set.filter(voter=self.user).delete()

    def test_anonymous(self):
        """api requires you to sign in to vote in poll"""
        self.logout_user()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This action is not available to guests.",
        })

    def test_empty_vote_json(self):
        """api validates if vote that user has made was empty"""
        self.delete_user_votes()

        response = self.client.post(
            self.api_link, '[]', content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ["You have to make a choice."],
        })

    def test_empty_vote_form(self):
        """api validates if vote that user has made was empty"""
        self.delete_user_votes()

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ["You have to make a choice."],
        })

    def test_malformed_vote(self):
        """api validates if vote that user has made was correctly structured"""
        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ['Expected a list of items but got type "dict".'],
        })

        response = self.post(self.api_link, data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ['Expected a list of items but got type "dict".'],
        })

        response = self.post(self.api_link, data='hello')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ['Expected a list of items but got type "str".'],
        })

        response = self.post(self.api_link, data=123)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ['Expected a list of items but got type "int".'],
        })

    def test_invalid_choices(self):
        """api validates if vote that user has made overlaps with allowed votes"""
        self.delete_user_votes()

        response = self.post(self.api_link, data=['lorem', 'ipsum'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ["One or more of poll choices were invalid."],
        })

    def test_too_many_choices(self):
        """api validates if vote that user has made overlaps with allowed votes"""
        self.poll.allowed_choices = 1
        self.poll.allow_revotes = True
        self.poll.save()

        response = self.post(self.api_link, data=['aaaaaaaaaaaa', 'bbbbbbbbbbbb'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'choices': ["This poll disallows voting for more than 1 choice."],
        })

    def test_revote(self):
        """api validates if user is trying to change vote in poll that disallows revoting"""
        response = self.post(self.api_link, data=['lorem', 'ipsum'])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You have already voted in this poll.",
        })

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_vote_in_closed_thread(self):
        """api validates is user has permission to vote poll in closed thread"""
        self.override_acl(category={'can_close_threads': 0})

        self.thread.is_closed = True
        self.thread.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This thread is closed. You can't vote in it.",
        })

        self.override_acl(category={'can_close_threads': 1})

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_vote_in_closed_category(self):
        """api validates is user has permission to vote poll in closed category"""
        self.override_acl(category={'can_close_threads': 0})

        self.category.is_closed = True
        self.category.save()

        self.delete_user_votes()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This category is closed. You can't vote in it.",
        })

        self.override_acl(category={'can_close_threads': 1})

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
        self.assertEqual(response.json(), {
            'detail': "This poll is over. You can't vote in it.",
        })
        
        self.poll.length = 50
        self.poll.save()

        response = self.post(self.api_link)
        self.assertEqual(response.status_code, 400)

    def test_fresh_vote(self):
        """api handles first vote in poll"""
        self.delete_user_votes()

        add_acl(self.user, self.poll)
        self.poll.acl['can_vote'] = False

        response = self.post(self.api_link, data=['aaaaaaaaaaaa', 'bbbbbbbbbbbb'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': self.poll.id,
            'poster_name': self.user.username,
            'posted_on': serialize_datetime(self.poll.posted_on),
            'length': 0,
            'question': "Lorem ipsum dolor met?",
            'allowed_choices': 2,
            'allow_revotes': False,
            'votes': 4,
            'is_public': False,
            'acl': self.poll.acl,
            'choices': [
                {
                    'hash': 'aaaaaaaaaaaa',
                    'label': 'Alpha',
                    'selected': True,
                    'votes': 2
                },
                {
                    'hash': 'bbbbbbbbbbbb',
                    'label': 'Beta',
                    'selected': True,
                    'votes': 1
                },
                {
                    'hash': 'gggggggggggg',
                    'label': 'Gamma',
                    'selected': False,
                    'votes': 1
                },
                {
                    'hash': 'dddddddddddd',
                    'label': 'Delta',
                    'selected': False,
                    'votes': 0
                },
            ],
            'api': {
                'index': self.poll.get_api_url(),
                'votes': self.poll.get_votes_api_url(),
            },
            'url': {
                'poster': self.user.get_absolute_url(),
            },
        })

        # validate state change
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.votes, 4)
        self.assertEqual(poll.choices, [
            {
                'hash': 'aaaaaaaaaaaa',
                'label': 'Alpha',
                'votes': 2
            },
            {
                'hash': 'bbbbbbbbbbbb',
                'label': 'Beta',
                'votes': 1
            },
            {
                'hash': 'gggggggggggg',
                'label': 'Gamma',
                'votes': 1
            },
            {
                'hash': 'dddddddddddd',
                'label': 'Delta',
                'votes': 0
            },
        ])

        self.assertEqual(poll.pollvote_set.count(), 4)

        # validate poll disallows for revote
        response = self.post(self.api_link, data=['aaaaaaaaaaaa'])
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "You have already voted in this poll.",
        })

    def test_vote_change(self):
        """api handles vote change"""
        self.poll.allow_revotes = True
        self.poll.save()

        add_acl(self.user, self.poll)

        response = self.post(self.api_link, data=['aaaaaaaaaaaa', 'bbbbbbbbbbbb'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'id': self.poll.id,
            'poster_name': self.user.username,
            'posted_on': serialize_datetime(self.poll.posted_on),
            'length': 0,
            'question': "Lorem ipsum dolor met?",
            'allowed_choices': 2,
            'allow_revotes': True,
            'votes': 4,
            'is_public': False,
            'acl': self.poll.acl,
            'choices': [
                {
                    'hash': 'aaaaaaaaaaaa',
                    'label': 'Alpha',
                    'selected': True,
                    'votes': 2
                },
                {
                    'hash': 'bbbbbbbbbbbb',
                    'label': 'Beta',
                    'selected': True,
                    'votes': 1
                },
                {
                    'hash': 'gggggggggggg',
                    'label': 'Gamma',
                    'selected': False,
                    'votes': 1
                },
                {
                    'hash': 'dddddddddddd',
                    'label': 'Delta',
                    'selected': False,
                    'votes': 0
                },
            ],
            'api': {
                'index': self.poll.get_api_url(),
                'votes': self.poll.get_votes_api_url(),
            },
            'url': {
                'poster': self.user.get_absolute_url(),
            },
        })

        # validate state change
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.votes, 4)
        self.assertEqual(poll.choices, [
            {
                'hash': 'aaaaaaaaaaaa',
                'label': 'Alpha',
                'votes': 2
            },
            {
                'hash': 'bbbbbbbbbbbb',
                'label': 'Beta',
                'votes': 1
            },
            {
                'hash': 'gggggggggggg',
                'label': 'Gamma',
                'votes': 1
            },
            {
                'hash': 'dddddddddddd',
                'label': 'Delta',
                'votes': 0
            },
        ])

        self.assertEqual(poll.pollvote_set.count(), 4)

        # validate poll allows for revote
        response = self.post(self.api_link, data=['aaaaaaaaaaaa'])
        self.assertEqual(response.status_code, 200)
