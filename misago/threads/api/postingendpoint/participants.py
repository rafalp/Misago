from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils import six
from django.utils.translation import ugettext as _, ungettext

from rest_framework import serializers

from misago.categories.models import PRIVATE_THREADS_ROOT_NAME

from . import PostingEndpoint, PostingMiddleware
from ...participants import add_owner, add_participant
from ...permissions import allow_message_user


class ParticipantsMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.mode == PostingEndpoint.START:
            return self.tree_name == PRIVATE_THREADS_ROOT_NAME
        return False

    def get_serializer(self):
        return ParticipantsSerializer(data=self.request.data, context={
            'user': self.user
        })

    def save(self, serializer):
        add_owner(self.thread, self.user)
        for user in serializer.users_cache:
            add_participant(self.request, self.thread, user)


class ParticipantsSerializer(serializers.Serializer):
    to = serializers.ListField(
       child=serializers.CharField()
    )

    def validate_to(self, usernames):
        clean_usernames = self.clean_usernames(usernames)
        self.users_cache = self.get_users(usernames)

    def clean_usernames(self, usernames):
        clean_usernames = []
        for name in usernames:
            clean_name = name.strip().lower()

            if clean_name == self.context['user'].slug:
                raise serializers.ValidationError(
                    _("You can't include yourself on the list of users to invite to new thread."))

            if clean_name and clean_name not in clean_usernames:
                clean_usernames.append(clean_name)

        max_participants = self.context['user'].acl['max_private_thread_participants']
        if max_participants and len(clean_usernames) > max_participants:
            message = ungettext(
                "You can't start private thread with more than %(users)s participant.",
                "You can't start private thread with more than %(users)s participants.",
                max_participants)
            raise forms.ValidationError(message % {'users': max_participants})

        return list(set(clean_usernames))

    def get_users(self, usernames):
        users = []
        for user in get_user_model().objects.filter(slug__in=usernames):
            try:
                allow_message_user(self.context['user'], user)
            except PermissionDenied as e:
                raise serializer.ValidationError(six.text_type(e))
            users.append(user)

        if len(usernames) != len(users):
            invalid_usernames = set(usernames) - set([u.slug for u in users])
            message = _("One or more users could not be found: %(usernames)s")
            raise serializers.ValidationError(
                message % {'usernames': ', '.join(invalid_usernames)})

        return users
