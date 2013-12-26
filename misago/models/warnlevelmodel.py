from django.core.cache import cache
from django.db import models
from django.utils.datastructures import SortedDict
from misago.thread import local

_thread_local = local()

class WarnLevelManager(models.Manager):
    def get_levels(self):
        try:
            return _thread_local._misago_warning_levels
        except AttributeError:
            _thread_local._misago_warning_levels = self.fetch_levels()
            return _thread_local._misago_warning_levels

    def get_level(self, level):
        return self.get_levels().get(level)

    def fetch_levels(self):
        from_cache = cache.get('warning_levels', 'nada')
        if from_cache != 'nada':
            return from_cache

        from_db = self.fetch_levels_from_db()
        cache.set('warning_levels', from_db)
        return from_db

    def fetch_levels_from_db(self):
        fetched_levels = SortedDict()
        for level in self.order_by('warning_level').iterator():
            fetched_levels[level.warning_level] = level
        return fetched_levels


class WarnLevel(models.Model):
    RESTRICT_NO = 0
    RESTRICT_MODERATOR_REVIEW = 1
    RESTRICT_DISALLOW = 2

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    warning_level = models.PositiveIntegerField(default=1, db_index=True)
    expires_after_minutes = models.PositiveIntegerField(default=0)
    restrict_posting_replies = models.PositiveIntegerField(default=RESTRICT_NO)
    restrict_posting_threads = models.PositiveIntegerField(default=RESTRICT_NO)

    objects = WarnLevelManager()

    class Meta:
        app_label = 'misago'

    def save(self, *args, **kwargs):
        super(WarnLevel, self).save(*args, **kwargs)
        cache.delete('warning_levels')

    def delete(self, *args, **kwargs):
        super(WarnLevel, self).delete(*args, **kwargs)
        cache.delete('warning_levels')
