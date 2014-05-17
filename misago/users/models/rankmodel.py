from django.db import models
from django.utils.translation import ugettext_lazy as _
from misago.core.utils import slugify


class Rank(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    style = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    is_special = models.BooleanField(default=False)
    is_tab = models.BooleanField(default=False)
    is_on_index = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    #roles = models.ManyToManyField('Role')

    class Meta:
        app_label = 'users'

    def __unicode__(self):
        return unicode(_(self.name))

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)
