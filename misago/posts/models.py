from django.db import models
from django.utils.translation import ugettext_lazy as _

class PostManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(date__gte=start).filter(date__lte=end)
    

class Post(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    thread = models.ForeignKey(Thread, related_name='+')
    user = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    user_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    post = models.TextField()
    post_preparsed = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    date = models.DateTimeField()
    attachments = models.BooleanField(default=False)
    attachments_list = models.CommaSeparatedIntegerField(max_length=255)
    edited = models.BooleanField(default=False)
    edits = models.PositiveIntegerField(default=0)
    edit_date = models.DateTimeField(null=True, blank=True)
    edit_reason = models.CharField(max_length=255, null=True, blank=True)
    edit_user = models.ForeignKey('users.User', related_name='+', null=True)
    edit_user_name = models.CharField(max_length=255, null=True, blank=True)
    edit_user_slug = models.SlugField(max_length=255, null=True, blank=True)
    reported = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    
    objects = PostManager()
    
    statistics_name = _('New Posts')
    
    def get_date(self):
        return self.date