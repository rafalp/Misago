from django.core.cache import cache
from django.utils import timezone
from misago.monitor.models import Item

class Monitor(object):
    def __init__(self):
        self._cache_deleted = False
        self._items = {}
        self.refresh()
            
    def refresh(self):
        self._items = cache.get('misago.monitor')
        if not self._items:
            self._items = {}
            for i in Item.objects.all():
                self._items[i.id] = [i.value, i.updated]
            cache.set('misago.monitor', self._items)

    def __contains__(self, key):
        return key in self._items

    def __getitem__(self, key):
        return self._items[key][0]

    def __setitem__(self, key, value):
        self._items[key][0] = value
        cache.set('misago.monitor', self._items)
        sync_item = Item(id=key, value=value, updated=timezone.now())
        sync_item.save(force_update=True)
        return value
        
    def __delitem__(self, key):
        pass
        
    def get(self, key, default=None):
        if not key in self._items:
            return default
        return self._items[key][0]
    
    def get_updated(self, key):
        if key in self._items:
            return self._items[key][1]
        return None
        
    def has_key(self, key):
        return key in self._items

    def keys(self):
        return self._items.keys()

    def values(self):
        return self._items.values()

    def items(self):
        return self._items.items()

    def iterkeys(self):
        return self._items.iterkeys()

    def itervalues(self):
        return self._items.itervalues()

    def iteritems(self):
        return self._items.iteritems()

