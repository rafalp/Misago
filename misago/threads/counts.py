from time import time

from django.conf import settings
from django.dispatch import receiver

from misago.threads.views.newthreads import NewThreads
from misago.threads.views.unreadthreads import UnreadThreads


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
            count = self.get_real_count()
            self.session[self.name] = count
        return count['threads']

    def is_cache_valid(self, cache):
        if cache.get('expires', 0) > time():
            return cache.get('user') == self.user.pk
        else:
            return False

    def get_expiration_timestamp(self):
        return time() + settings.MISAGO_CONTENT_COUNTING_FREQUENCY * 60

    def get_real_count(self):
        return {
            'threads': self.Threads(self.user).get_queryset().count(),
            'expires': self.get_expiration_timestamp()
        }

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


class NewThreadsCount(BaseCounter):
    Threads = NewThreads
    name = 'new_threads'


class UnreadThreadsCount(BaseCounter):
    Threads = UnreadThreads
    name = 'unread_threads'
