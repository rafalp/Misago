from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from misago.thread import local

_thread_local = local()

def load_monitor():
    from misago.models import MonitorItem
    monitor = cache.get('monitor', {})
    if not monitor:
        for i in MonitorItem.objects.all():
            monitor[i.id] = [i.value, i.updated, i.type]
        cache.set('monitor', monitor)
    return monitor


def refresh_monitor():
    _thread_local.monitor = load_monitor()


class Monitor(object):
    def monitor(self):
        try:
            return _thread_local.monitor
        except AttributeError:
            _thread_local.monitor = load_monitor()
            return _thread_local.monitor

    def entry(self, key):
        try:
            return self.monitor()[key]
        except KeyError:
            raise Exception(u"Monitor entry \"%s\" could not be found." % key)

    def __contains__(self, key):
        return key in self.monitor()

    def __getitem__(self, key):
        return self.entry(key)[0]

    def __getattr__(self, key):
        return self.entry(key)[0]

    def __setitem__(self, key, value):
        _thread_local.monitor_update.append((key, value))
        return value

    def increase(self, key, i=1):
        _thread_local.monitor_update.append((key, self[key] + i))

    def decrease(self, key, i=1):
        _thread_local.monitor_update.append((key, self[key] - i))

    def get(self, key, default=None):
        if not key in self.monitor():
            return default
        return self.entry(key)[0]

    def updated(self, key):
        if key in self.monitor():
            return self.entry(key)[1]
        return None

    def expired(self, key, seconds=5):
        return self.entry(key)[1] < (timezone.now() - timedelta(seconds=seconds))

    def has_key(self, key):
        return key in self.entry()

    def keys(self):
        return self.entry().keys()

    def values(self):
        return self.entry().values()

    def items(self):
        return self.entry().items()

    def iterkeys(self):
        return self.entry().iterkeys()

    def itervalues(self):
        return self.entry().itervalues()

    def iteritems(self):
        return self.entry().iteritems()


class UpdatingMonitor(object):
    def __enter__(self):
        _thread_local.monitor_update = []

    def __exit__(self, type, value, traceback):
        if _thread_local.monitor_update:
            from misago.models import MonitorItem
            for key, value in _thread_local.monitor_update:
                MonitorItem.objects.filter(pk=key).update(_value=value, updated=timezone.now())
            cache.delete('monitor')
            _thread_local.monitor_update = None


monitor = Monitor()
