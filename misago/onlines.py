from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from misago.models import Session

class MembersOnline(object):
    def __init__(self, monitor, frequency=180):
        self.monitor = monitor
        self.frequency = frequency
        self._members = int(monitor['online_members'])
        self._all = int(monitor['online_all'])
        self._om = self._members
        self._oa = self._all
        if (monitor.expired('online_all', frequency) or
                monitor.expired('online_members', frequency)):
            self.count_sessions()

    def count_sessions(self):
        queryset = Session.objects.filter(matched=True).filter(crawler__isnull=True).filter(last__gte=timezone.now() - timedelta(seconds=self.frequency))
        self._all = queryset.count()
        self._members = queryset.filter(user__isnull=False).count()
        cache.delete_many(['team_users_online', 'ranks_online'])

    def new_session(self):
        self._all += 1

    def sign_in(self):
        self._members += 1

    def sign_out(self):
        if self._members:
            self._members -= 1

    @property
    def all(self):
        return self._all

    @property
    def members(self):
        return self._members

    def sync(self):
        if self._members != self._om:
            self.monitor['online_members'] = self._members
        if self._all != self._oa:
            self.monitor['online_all'] = self._all

    def stats(self, request=None):
        # Are we request-aware?
        if not request:
            return {
                    'members': self.members,
                    'all': self.all,
                   }

        online = self.stats()

        # Here we check for signs that online stats are out of sync
        try:
            if not online['members'] and request.user.is_authenticated():
                raise ValueError()
            if online['members'] > online['all']:
                raise ValueError()
            if (online['members'] == online['all'] and
                    not request.user.is_authenticated()):
                raise ValueError()
            return online
        except ValueError:
            if request.session.matched:
                self.count_sessions()
                return self.stats()
            else:
                if request.user.is_authenticated() and not online['members']:
                    online['members'] += 1
                if online['members'] > online['all']:
                    online['all'] = online['members']
                if request.user.is_anonymous() and online['members'] == online['all']:
                    online['all'] += 1
                return online

