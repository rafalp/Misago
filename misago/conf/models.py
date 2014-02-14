import base64
from django.db import models
try:
    import cPickle as pickle
except ImportError:
    import pickle


class SettingsGroup(models.Model):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


# Setting hydrate/dehydrate functions

def hydrate_string(dry_value):
    return dry_value


def dehydrate_string(wet_value):
    return wet_value


def hydrate_bool(dry_value):
    return dry_value == 'True'


def dehydrate_bool(wet_value):
    return 'True' if dry_value else 'False'


def hydrate_int(dry_value):
    return int(dry_value)


def dehydrate_int(wet_value):
    return unicode(wet_value)


def hydrate_list(dry_value):
    return dry_value.split(',')


def dehydrate_list(wet_value):
    return ','.join(wet_value)


VALUE_HYDRATORS = {
    'string': (hydrate_string, dehydrate_string),
    'bool': (hydrate_bool, dehydrate_bool),
    'int': (hydrate_int, dehydrate_int),
    'list': (hydrate_list, dehydrate_list),
}


def hydrate_value(python_type, dry_value):
    value_hydrator = VALUE_HYDRATORS[python_type][0]
    return value_hydrator(dry_value)


def dehydrate_value(python_type, wet_value):
    value_dehydrator = VALUE_HYDRATORS[python_type][1]
    return value_dehydrator(wet_value)


class Setting(models.Model):
    group = models.ForeignKey('SettingsGroup')
    setting = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    legend = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0, db_index=True)
    dry_value = models.TextField(null=True, blank=True)
    default_value = models.TextField(null=True, blank=True)
    python_type = models.CharField(max_length=255)
    is_lazy = models.BooleanField(default=False)
    form_field = models.CharField(max_length=255)
    pickled_field_extra = models.TextField(null=True, blank=True)

    @property
    def value(self):
        return hydrate_value(self.python_type, self.dry_value)

    @value.setter
    def value(self, new_value):
        return dehydrate_value(self.python_type, self.new_value)

    @property
    def has_custom_value(self):
        return self.default_value and self.dry_value != self.default_value

    @property
    def field_extra(self):
        if self.pickled_field_extra:
            return pickle.loads(base64.decodestring(self.pickled_field_extra))
        else:
            return {}

    @field_extra.setter
    def field_extra(self, new_extra):
        pickled_extra = pickle.dumps(choices_cache, pickle.HIGHEST_PROTOCOL)
        self.pickled_field_extra = base64.encodestring(pickled_extra)
