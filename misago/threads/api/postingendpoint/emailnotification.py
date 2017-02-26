from django.utils.translation import ugettext as _

from misago.core.mail import build_mail, send_messages
from misago.threads.permissions import can_see_post, can_see_thread

from . import PostingEndpoint, PostingMiddleware


class EmailNotificationMiddleware(PostingMiddleware):
    def __init__(self, **kwargs):
        super(EmailNotificationMiddleware, self).__init__(**kwargs)

        self.previous_last_post_on = self.thread.last_post_on

    def use_this_middleware(self):
        return self.mode == PostingEndpoint.REPLY

    def post_save(self, serializer):
        queryset = self.thread.subscription_set.filter(
            send_email=True,
            last_read_on__gte=self.previous_last_post_on,
        ).exclude(user=self.user).select_related('user')

        notifications = []
        for subscription in queryset.iterator():
            if self.notify_user_of_post(subscription.user):
                notifications.append(self.build_mail(subscription.user))

        if notifications:
            send_messages(notifications)

    def notify_user_of_post(self, subscriber):
        see_thread = can_see_thread(subscriber, self.thread)
        see_post = can_see_post(subscriber, self.post)
        return see_thread and see_post

    def build_mail(self, subscriber):
        if subscriber.id == self.thread.starter_id:
            subject = _('%(user)s has replied to your thread "%(thread)s"')
        else:
            subject = _('%(user)s has replied to thread "%(thread)s" that you are watching')

        subject_formats = {'user': self.user.username, 'thread': self.thread.title}

        return build_mail(
            self.request,
            subscriber,
            subject % subject_formats,
            'misago/emails/thread/reply',
            {
                'thread': self.thread,
                'post': self.post,
            },
        )
