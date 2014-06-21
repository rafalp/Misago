from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from misago.admin import site
from misago.acl import version as acl_version
from misago.core.utils import slugify


class RankManager(models.Manager):
    def default(self):
        return self.get(is_default=True)

    def make_rank_default(self, rank):
        with transaction.atomic():
            self.filter(is_default=True).update(is_default=False)
            rank.is_default = True
            rank.save(update_fields=['is_default'])


class Rank(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ManyToManyField('misago_acl.Role', null=True, blank=True)
    css_class = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_tab = models.BooleanField(default=False)
    is_on_index = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    objects = RankManager()

    class Meta:
        get_latest_by = 'order'

    def __unicode__(self):
        return unicode(_(self.name))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_order()
        else:
            acl_version.invalidate()
        return super(Rank, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        acl_version.invalidate()
        return super(Rank, self).delete(*args, **kwargs)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_order(self):
        try:
            self.order = Rank.objects.latest('order').order + 1
        except Rank.DoesNotExist:
            self.order = 0


"""register model in misago admin"""
site.add_node(
    parent='misago:admin:users',
    namespace='misago:admin:users:ranks',
    link='misago:admin:users:ranks:index',
    name=_("Ranks"),
    after='misago:admin:users:accounts:index',
    icon='fa fa-graduation-cap')
