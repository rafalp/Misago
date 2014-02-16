import base64
from django.db import models
from misago.conf import hydrators
try:
    import cPickle as pickle
except ImportError:
    import pickle


class SettingsGroup(models.Model):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Setting(models.Model):
    group = models.ForeignKey(SettingsGroup)
    setting = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    legend = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0, db_index=True)
    dry_value = models.TextField(null=True, blank=True)
    default_value = models.TextField(null=True, blank=True)
    python_type = models.CharField(max_length=255, default='string')
    is_lazy = models.BooleanField(default=False)
    form_field = models.CharField(max_length=255, default='text')
    pickled_field_extra = models.TextField(null=True, blank=True)

    @property
    def value(self):
        if not self.dry_value and self.default_value:
            return hydrators.hydrate_value(self.python_type,
                                           self.default_value)
        else:
            return hydrators.hydrate_value(self.python_type,
                                           self.dry_value)

    @value.setter
    def value(self, new_value):
        if new_value != None:
            self.dry_value = hydrators.dehydrate_value(self.python_type,
                                                       new_value)
        else:
            self.dry_value = self.default_value
        return self.value

    @property
    def has_custom_value(self):
        return self.dry_value and self.dry_value != self.default_value

    @property
    def field_extra(self):
        if self.pickled_field_extra:
            return pickle.loads(base64.decodestring(self.pickled_field_extra))
        else:
            return {}

    @field_extra.setter
    def field_extra(self, new_extra):
        if new_extra:
            pickled_extra = pickle.dumps(new_extra, pickle.HIGHEST_PROTOCOL)
            self.pickled_field_extra = base64.encodestring(pickled_extra)
