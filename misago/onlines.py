from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from misago.models import Session
from misago.monitor import monitor, UpdatingMonitor

class MembersOnline(object):
    def __init__(self, mode, frequency=180):
        self.frequency = frequency
        self._mode = mode
        self._members = monitor['online_members']
        self._all = monitor['online_all']
        self._om = self._members
        self._oa = self._all
        if (self._mode != 'no' or monitor.expired('online_all', frequency) or
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
        if self._mode == 'snap':
            with UpdatingMonitor() as cm:
                if self._members != self._om:
                    monitor['online_members'] = self._members
                if self._all != self._oa:
                    monitor['online_all'] = self._all

    def stats(self, request):
        stat = {
                'members': self.members,
                'all': self.all,
               }

        if not request.user.is_crawler():
            if not stat['members'] and request.user.is_authenticated():
                stat['members'] += 1
                stat['all'] += 1
            if not stat['all']:
                stat['all'] += 1        
        return stat