from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_lazy as _
from misago.admin import site
from misago.core.utils import slugify


class Rank(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    style = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_tab = models.BooleanField(default=False)
    is_on_index = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    #roles = models.ManyToManyField('Role')

    class Meta:
        app_label = 'users'
        get_latest_by = 'order'

    def __unicode__(self):
        return unicode(_(self.name))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_order()
        return super(Rank, self).save(*args, **kwargs)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_order(self):
        try:
            self.order = Rank.objects.latest('order').order + 1
        except Rank.DoesNotExist:
            self.order = 0

    def next(self):
        try:
            return Rank.objects.filter(order__gt=self.order).earliest('order')
        except Rank.DoesNotExist:
            return None

    def prev(self):
        try:
            return Rank.objects.filter(order__lt=self.order).latest('order')
        except Rank.DoesNotExist:
            return None


"""register model in misago admin"""
site.add_node(
    parent='misago:admin:users',
    namespace='misago:admin:users:ranks',
    link='misago:admin:users:ranks:index',
    name=_("Ranks"),
    icon='fa fa-graduation-cap')
