from django.db.utils import DatabaseError
from django.core.cache import cache
from misago.models import Setting

class DBSettings(object):
    """
    Database-stored high-level and "safe" settings controller
    """
    def __init__(self):
        self._settings = {}
        self._models = {}
        self.refresh()

    def refresh(self):
        self._models = cache.get('settings')
        if not self._models:
            self._models = {}
            try:
                for i in Setting.objects.all():
                    self._models[i.pk] = i
                    self._settings[i.pk] = i.get_value()
            except DatabaseError:
                pass
        else:
            for i, model in self._models.items():
                self._settings[i] = model.get_value()

    def __getattr__(self, key):
        return self._settings[key]

    def __contains__(self, key):
        return key in self._settings.keys()

    def __getitem__(self, key):
        return self._settings[key]

    def __setitem__(self, key, value):
        if key in self._settings:
            self._models[key].set_value(value)
            self._models[key].save(force_update=True)
            self._settings[key] = value
        return value

    def __delitem__(self, key):
        pass

    def get(self, key, default=None):
        try:
            return self._settings[key]
        except KeyError:
            return None

    def has_key(self, key):
        return key in self._settings.keys()

    def keys(self):
        return self._settings.keys()

    def values(self):
        return self._settings.values()

    def items(self):
        return self._settings.items()

    def iterkeys(self):
        return self._settings.iterkeys()

    def itervalues(self):
        return self._settings.itervalues()

    def iteritems(self):
        return self._settings.iteritems()
