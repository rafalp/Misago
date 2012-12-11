from django.db import models
from django.utils.translation import ugettext_lazy as _

class ThreadManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(start__gte=start).filter(start__lte=end)


class Thread(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default=0)
    start = models.DateTimeField(default=0)
    start_post = models.ForeignKey('Post', related_name='+', null=True, blank=True)
    start_poster = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    start_poster_name = models.CharField(max_length=255)
    start_poster_slug = models.SlugField(max_length=255)
    start_poster_style = models.CharField(max_length=255)
    last = models.DateTimeField()
    last_post = models.ForeignKey('Post', related_name='+', null=True, blank=True)
    last_poster = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_poster_style = models.CharField(max_length=255, null=True, blank=True)
    poster_styles_list = models.CharField(max_length=255, null=True, blank=True)
    hidden = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    
    objects = ThreadManager()
    
    statistics_name = _('New Threads')
        
    def get_date(self):
        return self.start