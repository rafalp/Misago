from django.core.cache import cache
from django.db import models
from django.utils.datastructures import SortedDict
from misago.signals import (merge_thread, move_forum_content,
                            move_thread, remove_thread_prefix)
from misago.thread import local

_thread_local = local()

class ThreadPrefixManager(models.Manager):
    def flush_cache(self):
        cache.delete('threads_prefixes')

    def make_cache(self):
        prefixes = cache.get('threads_prefixes', 'nada')
        if prefixes == 'nada':
            prefixes = []
            for prefix in ThreadPrefix.objects.order_by('name').iterator():
                prefix.forums_pks = [f.pk for f in prefix.forums.iterator()]
                prefixes.append(prefix)
            cache.set('threads_prefixes', prefixes, None)
        dict_result = SortedDict()
        for prefix in prefixes:
            dict_result[prefix.pk] = prefix
        return dict_result

    def all_prefixes(self):
        try:
            return _thread_local.misago_thread_prefixes
        except AttributeError:
            _thread_local.misago_thread_prefixes = self.make_cache()
        return _thread_local.misago_thread_prefixes

    def forum_prefixes(self, forum):
        forum_prefixes = []
        for prefix in self.all_prefixes().values():
            if forum.pk in prefix.forums_pks:
                forum_prefixes.append((prefix.pk, prefix))
        return SortedDict(forum_prefixes)

    def prefix_in_forum(self, prefix, forum):
        forum_prefixes = self.forum_prefixes(forum)
        return prefix in forum_prefixes


class ThreadPrefix(models.Model):
    forums = models.ManyToManyField('Forum')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    style = models.CharField(max_length=255)

    objects = ThreadPrefixManager()

    class Meta:
        app_label = 'misago'

    def save(self, *args, **kwargs):
        ThreadPrefix.objects.flush_cache()
        super(ThreadPrefix, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ThreadPrefix.objects.flush_cache()
        super(ThreadPrefix, self).delete(*args, **kwargs)

    def update_forums(self, new_forums):
        current_forums = self.forums.all()

        removed_forums = []
        for forum in current_forums:
            if not forum in new_forums:
                removed_forums.append(forum)

        if removed_forums:
            remove_thread_prefix.send(sender=self, forums=removed_forums)

        self.forums.clear()
        for forum in new_forums:
            self.forums.add(forum)


def move_forum_content_handler(sender, **kwargs):
    old_forum_prefixes = ThreadPrefix.objects.forum_prefixes(sender)
    new_forum_prefixes = ThreadPrefix.objects.forum_prefixes(kwargs['move_to'])
    bad_prefixes = list(set(new_forum_prefixes) - set(old_forum_prefixes))

    if bad_prefixes:
        sender.thread_set.filter(prefix__in=bad_prefixes).update(prefix=None)

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads_prefixes")


def move_thread_handler(sender, **kwargs):
    if sender.prefix and not ThreadPrefix.objects.prefix_in_forum(sender.prefix, kwargs['move_to']):
        sender.prefix = None

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_prefixes")


def merge_thread_handler(sender, **kwargs):
    if kwargs['new_thread'].prefix and not ThreadPrefix.objects.prefix_in_forum(kwargs['new_thread'].prefix, kwargs['new_thread'].forum):
        kwargs['new_thread'].prefix = None

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_prefixes")