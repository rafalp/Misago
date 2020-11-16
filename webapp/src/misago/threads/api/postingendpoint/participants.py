from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from rest_framework import serializers

from . import PostingEndpoint, PostingMiddleware
from ....acl import useracl
from ....categories import PRIVATE_THREADS_ROOT_NAME
from ...participants import add_participants, set_owner
from ...permissions import allow_message_user

User = get_user_model()


class ParticipantsMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        if self.mode == PostingEndpoint.START:
            return self.tree_name == PRIVATE_THREADS_ROOT_NAME
        return False

    def get_serializer(self):
        return ParticipantsSerializer(
            data=self.request.data,
            context={
                "request": self.request,
                "user": self.user,
                "user_acl": self.user_acl,
            },
        )

    def save(self, serializer):
        set_owner(self.thread, self.user)
        add_participants(self.request, self.thread, serializer.users_cache)


class ParticipantsSerializer(serializers.Serializer):
    to = serializers.ListField(child=serializers.CharField(), required=True)

    def validate_to(self, usernames):
        clean_usernames = self.clean_usernames(usernames)
        self.users_cache = self.get_users(clean_usernames)

    def clean_usernames(self, usernames):
        clean_usernames = []
        for name in usernames:
            clean_name = name.strip().lower()

            if clean_name == self.context["user"].slug:
                raise serializers.ValidationError(
                    _(
                        "You can't include yourself on the "
                        "list of users to invite to new thread."
                    )
                )

            if clean_name and clean_name not in clean_usernames:
                clean_usernames.append(clean_name)

        if not clean_usernames:
            raise serializers.ValidationError(_("You have to enter user names."))

        max_participants = self.context["user_acl"]["max_private_thread_participants"]
        if max_participants and len(clean_usernames) > max_participants:
            # pylint: disable=line-too-long
            message = ngettext(
                "You can't add more than %(users)s user to private thread (you've added %(added)s).",
                "You can't add more than %(users)s users to private thread (you've added %(added)s).",
                max_participants,
            )
            raise serializers.ValidationError(
                message % {"users": max_participants, "added": len(clean_usernames)}
            )

        return list(set(clean_usernames))

    def get_users(self, usernames):
        users = []
        for user in User.objects.filter(slug__in=usernames):
            try:
                user_acl = useracl.get_user_acl(
                    user, self.context["request"].cache_versions
                )
                allow_message_user(self.context["user_acl"], user, user_acl)
            except PermissionDenied as e:
                raise serializers.ValidationError(str(e))
            users.append(user)

        if len(usernames) != len(users):
            invalid_usernames = set(usernames) - {u.slug for u in users}
            sorted_usernames = sorted(invalid_usernames)

            message = _("One or more users could not be found: %(usernames)s")
            raise serializers.ValidationError(
                message % {"usernames": ", ".join(sorted_usernames)}
            )

        return users
