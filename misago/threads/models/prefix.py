from django.db import models

from misago.core.cache import cache
from misago.core.utils import slugify


CACHE_NAME = 'misago_threads_prefixes'


class PrefixManager(models.Manager):
    def get_forum_prefixes(self, forum):
        prefixes = []
        for prefix in self.get_cached_prefixes():
            if forum.pk in prefix.forums_ids:
                prefixes.append(prefix)
        return prefixes

    def get_cached_prefixes_dict(self):
        prefixes_dict = {}
        for prefix in self.get_cached_prefixes():
            prefixes_dict[prefix.pk] = prefix
        return prefixes_dict

    def get_cached_prefixes(self):
        prefixes = cache.get(CACHE_NAME, 'nada')
        if prefixes == 'nada':
            prefixes = []
            prefixes_qs = self.all().prefetch_related('forums')
            for prefix in prefixes_qs.order_by('name'):
                prefix.forums_ids = [f.pk for f in prefix.forums.all()]
                prefixes.append(prefix)
            cache.set(CACHE_NAME, prefixes)
        return prefixes

    def clear_cache(self):
        cache.delete(CACHE_NAME)


class Prefix(models.Model):
    forums = models.ManyToManyField('misago_forums.Forum')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    css_class = models.CharField(max_length=255, null=True, blank=True)

    objects = PrefixManager()

    def save(self, *args, **kwargs):
        if self.pk:
            self.strip_inavailable_prefixes()
        Prefix.objects.clear_cache()
        return super(Prefix, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Prefix.objects.clear_cache()
        return super(Prefix, self).delete(*args, **kwargs)

    def strip_inavailable_prefixes(self):
        qs = self.thread_set
        if self.forums:
            qs = qs.exclude(forum__in=self.forums.all())
        qs.update(prefix=None)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)
