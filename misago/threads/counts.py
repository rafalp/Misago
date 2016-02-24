from time import time

from django.conf import settings
from django.db.models import F
from django.dispatch import receiver

from misago.categories.models import Category

from misago.threads.views.moderatedcontent import ModeratedContent
from misago.threads.views.newthreads import NewThreads
from misago.threads.views.unreadthreads import UnreadThreads
from misago.threads.views.privatethreads import PrivateThreads


class BaseCounter(object):
    Threads = None
    name = None

    def __init__(self, user, session):
        self.user = user
        self.session = session
        self.count = self.get_cached_count()

    def __int__(self):
        return self.count

    def __unicode__(self):
        return unicode(self.count)

    def __nonzero__( self) :
        return bool(self.count)

    def get_cached_count(self):
        count = self.session.get(self.name, None)

        if not count or not self.is_cache_valid(count):
            count = self.get_current_count_dict()
            self.session[self.name] = count
        return count['threads']

    def is_cache_valid(self, cache):
        if cache.get('expires', 0) > time():
            return cache.get('user') == self.user.pk
        else:
            return False

    def get_expiration_timestamp(self):
        return time() + settings.MISAGO_CONTENT_COUNTING_FREQUENCY * 60

    def get_current_count_dict(self):
        return {
            'user': self.user.pk,
            'threads': self.count_threads(),
            'expires': self.get_expiration_timestamp()
        }

    def count_threads(self):
        return self.Threads(self.user).get_queryset().count()

    def set(self, count):
        self.count = count
        self.session[self.name] = {
            'user': self.user.pk,
            'threads': count,
            'expires': self.get_expiration_timestamp()
        }

    def decrease(self):
        if self.count > 0:
            self.count -= 1
            self.session[self.name] = {
                'user': self.user.pk,
                'threads': self.count,
                'expires': self.session[self.name]['expires']
            }


class ModeratedCount(BaseCounter):
    Threads = ModeratedContent
    name = 'moderated_content'


class NewThreadsCount(BaseCounter):
    Threads = NewThreads
    name = 'new_threads'


class UnreadThreadsCount(BaseCounter):
    Threads = UnreadThreads
    name = 'unread_threads'


def sync_user_unread_private_threads_count(user):
    if not user.sync_unread_private_threads:
        return

    threads_qs = PrivateThreads(user).get_queryset()

    all_threads_count = threads_qs.count()

    read_qs = user.threadread_set.filter(category=Category.objects.private_threads())
    read_qs = read_qs.filter(last_read_on__gte=F('thread__last_post_on'))
    read_threads_count = read_qs.count()

    user.unread_private_threads = all_threads_count - read_threads_count
    if user.unread_private_threads < 0:
        # we may end with negative count because of race conditions in counts
        user.unread_private_threads = 0

    user.sync_unread_private_threads = False
    user.save(update_fields=[
        'unread_private_threads', 'sync_unread_private_threads'
    ])
