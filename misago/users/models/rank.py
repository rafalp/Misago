from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

from misago.acl import version as acl_version
from misago.core.utils import slugify


class RankManager(models.Manager):
    def get_default(self):
        return self.get(is_default=True)

    def make_rank_default(self, rank):
        with transaction.atomic():
            self.filter(is_default=True).update(is_default=False)
            rank.is_default = True
            rank.save(update_fields=['is_default'])


@python_2_unicode_compatible
class Rank(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ManyToManyField('misago_acl.Role', blank=True)
    css_class = models.CharField(max_length=255, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_tab = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    objects = RankManager()

    class Meta:
        get_latest_by = 'order'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_order()
        else:
            acl_version.invalidate()
        return super(Rank, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        acl_version.invalidate()
        return super(Rank, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('misago:users-rank', kwargs={'slug': self.slug})

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_order(self):
        try:
            self.order = Rank.objects.latest('order').order + 1
        except Rank.DoesNotExist:
            self.order = 0
