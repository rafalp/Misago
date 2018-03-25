from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse

from misago.categories.models import Category
from misago.conf import settings
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads import testutils
from misago.threads.api.postendpoints.patch_post import patch_is_liked
from misago.threads.models import Post
from misago.threads.participants import (
    add_participant, change_owner, make_participants_aware, remove_participant, set_owner)


UserModel = get_user_model()


def get_mock_user():
    seed = UserModel.objects.count() + 1
    return UserModel.objects.create_user('bob%s' % seed, 'user%s@test.com' % seed, 'Pass.123')


class AnonymizeEventsTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(AnonymizeEventsTests, self).setUp()
        self.factory = RequestFactory()

        category = Category.objects.get(slug='first-category')
        self.thread = testutils.post_thread(category)

    def get_request(self, user=None):
        request = self.factory.get('/customer/details')
        request.user = user or self.user
        request.user_ip = '127.0.0.1'

        request.include_frontend_context = False
        request.frontend_context = {}

        return request

    def test_anonymize_changed_owner_event(self):
        """changed owner event is anonymized by user.anonymize_content"""
        user = get_mock_user()
        request = self.get_request()

        set_owner(self.thread, self.user)
        make_participants_aware(self.user, self.thread)
        change_owner(request, self.thread, user)

        user.anonymize_content()

        event = Post.objects.get(event_type='changed_owner')
        self.assertEqual(event.event_context, {
            'user': {
                'id': None,
                'username': user.username,
                'url': reverse('misago:users'),
            },
        })

    def test_anonymize_added_participant_event(self):
        """added participant event is anonymized by user.anonymize_content"""
        user = get_mock_user()
        request = self.get_request()

        set_owner(self.thread, self.user)
        make_participants_aware(self.user, self.thread)
        add_participant(request, self.thread, user)

        user.anonymize_content()

        event = Post.objects.get(event_type='added_participant')
        self.assertEqual(event.event_context, {
            'user': {
                'id': None,
                'username': user.username,
                'url': reverse('misago:users'),
            },
        })

    def test_anonymize_owner_left_event(self):
        """owner left event is anonymized by user.anonymize_content"""
        user = get_mock_user()
        request = self.get_request(user)

        set_owner(self.thread, user)
        make_participants_aware(user, self.thread)
        add_participant(request, self.thread, self.user)

        make_participants_aware(user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_content()

        event = Post.objects.get(event_type='owner_left')
        self.assertEqual(event.event_context, {
            'user': {
                'id': None,
                'username': user.username,
                'url': reverse('misago:users'),
            },
        })

    def test_anonymize_removed_owner_event(self):
        """removed owner event is anonymized by user.anonymize_content"""
        user = get_mock_user()
        request = self.get_request()

        set_owner(self.thread, user)
        make_participants_aware(user, self.thread)
        add_participant(request, self.thread, self.user)
        
        make_participants_aware(user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_content()

        event = Post.objects.get(event_type='removed_owner')
        self.assertEqual(event.event_context, {
            'user': {
                'id': None,
                'username': user.username,
                'url': reverse('misago:users'),
            },
        })

    def test_anonymize_participant_left_event(self):
        """participant left event is anonymized by user.anonymize_content"""
        user = get_mock_user()
        request = self.get_request(user)

        set_owner(self.thread, self.user)
        make_participants_aware(user, self.thread)
        add_participant(request, self.thread, user)

        make_participants_aware(user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_content()

        event = Post.objects.get(event_type='participant_left')
        self.assertEqual(event.event_context, {
            'user': {
                'id': None,
                'username': user.username,
                'url': reverse('misago:users'),
            },
        })
        
    def test_anonymize_removed_participant_event(self):
        """removed participant event is anonymized by user.anonymize_content"""
        user = get_mock_user()
        request = self.get_request()

        set_owner(self.thread, self.user)
        make_participants_aware(self.user, self.thread)
        add_participant(request, self.thread, user)

        make_participants_aware(self.user, self.thread)
        remove_participant(request, self.thread, user)

        user.anonymize_content()

        event = Post.objects.get(event_type='removed_participant')
        self.assertEqual(event.event_context, {
            'user': {
                'id': None,
                'username': user.username,
                'url': reverse('misago:users'),
            },
        })


class AnonymizeLikesTests(AuthenticatedUserTestCase):
    def setUp(self):
        super(AnonymizeLikesTests, self).setUp()
        self.factory = RequestFactory()

    def get_request(self, user=None):
        request = self.factory.get('/customer/details')
        request.user = user or self.user
        request.user_ip = '127.0.0.1'

        return request

    def test_anonymize_user_likes(self):
        """post's last like is anonymized by user.anonymize_content"""
        category = Category.objects.get(slug='first-category')
        thread = testutils.post_thread(category)
        post = testutils.reply_thread(thread)
        post.acl = {'can_like': True}

        user = get_mock_user()

        patch_is_liked(self.get_request(self.user), post, 1)
        patch_is_liked(self.get_request(user), post, 1)

        user.anonymize_content()

        last_likes = Post.objects.get(pk=post.pk).last_likes
        self.assertEqual(last_likes, [
            {
                'id': None,
                'username': user.username,
            },
            {
                'id': self.user.id,
                'username': self.user.username,
            },
        ])