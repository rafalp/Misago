from django.utils.translation import gettext as _

from . import PostingEndpoint, PostingMiddleware
from ....acl import useracl
from ....core.mail import build_mail, send_messages
from ...permissions import can_see_post, can_see_thread


class EmailNotificationMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.previous_last_post_on = self.thread.last_post_on

    def use_this_middleware(self):
        return self.mode == PostingEndpoint.REPLY

    def post_save(self, serializer):
        queryset = (
            self.thread.subscription_set.filter(
                send_email=True, last_read_on__gte=self.previous_last_post_on
            )
            .exclude(user=self.user)
            .select_related("user")
        )

        notifications = []
        for subscription in queryset.iterator():
            if self.subscriber_can_see_post(subscription.user):
                notifications.append(self.build_mail(subscription.user))

        if notifications:
            send_messages(notifications)

    def subscriber_can_see_post(self, subscriber):
        user_acl = useracl.get_user_acl(subscriber, self.request.cache_versions)
        see_thread = can_see_thread(user_acl, self.thread)
        see_post = can_see_post(user_acl, self.post)
        return see_thread and see_post

    def build_mail(self, subscriber):
        if subscriber.id == self.thread.starter_id:
            subject = _('%(user)s has replied to your thread "%(thread)s"')
        else:
            subject = _(
                '%(user)s has replied to thread "%(thread)s" that you are watching'
            )

        subject_formats = {"user": self.user.username, "thread": self.thread.title}

        return build_mail(
            subscriber,
            subject % subject_formats,
            "misago/emails/thread/reply",
            sender=self.user,
            context={
                "settings": self.request.settings,
                "thread": self.thread,
                "post": self.post,
            },
        )
