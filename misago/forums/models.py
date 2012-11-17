from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Forum(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    position = models.IntegerField()   
    role = models.CharField(max_length=12, choices=(
        ('cat', 'Category'),
        ('for', 'Forum'),
        ('red', 'Redirect')
    ))
    special = models.CharField(max_length=255,null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    style = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    description_preparsed = models.TextField(null=True, blank=True)
    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    last_thread = models.ForeignKey('Thread', related_name='+', null=True, blank=True)
    last_thread_name = models.CharField(max_length=255, null=True, blank=True)
    last_thread_slug = models.SlugField(null=True, blank=True)
    last_thread_date = models.DateTimeField(null=True, blank=True)
    last_poster = models.ForeignKey('users.User', related_name='+')
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_poster_style = models.CharField(max_length=255, null=True, blank=True)
    closed = models.BooleanField(default=False)
    
    class MPTTMeta:
            order_insertion_by = ['position']


class ThreadManager(models.Manager):
    def filter_overview(self, start, end):
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


class PostManager(models.Manager):
    def filter_overview(self, start, end):
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


class AttachmentType(models.Model):
    mime = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    
        
class Attachment(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    thread = models.ForeignKey(Thread, related_name='+')
    post = models.ForeignKey(Post, related_name='+')
    type = models.ForeignKey(AttachmentType, related_name='+')
    user = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    created = models.DateTimeField()
    size = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=settings.MEDIA_ROOT + '/attachments/%m_%Y/',max_length=255)
    downloads = models.PositiveIntegerField(default=0)
    
    
class Poll(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    thread = models.ForeignKey(Thread, related_name='+')
    name = models.CharField(max_length=255)
    name_slug = models.SlugField(max_length=255)
    user = models.ForeignKey('users.User', related_name='+')
    user_name = models.CharField(max_length=255)
    user_slug = models.SlugField(max_length=255)
    public = models.BooleanField(default=False)
    multiple = models.BooleanField(default=False)
    changing = models.BooleanField(default=False)
    created = models.DateTimeField()
    length = models.PositiveIntegerField(default=0)
    votes = models.PositiveIntegerField(default=0)
    
    
class Vote(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    thread = models.ForeignKey(Thread, related_name='+')
    poll = models.ForeignKey(Poll, related_name='+')
    user = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    ip = models.GenericIPAddressField()
    option = models.PositiveIntegerField()
    
   
class Moderator(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    group = models.ForeignKey('users.Group', related_name='+', null=True, blank=True)
    user = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    
    
class Report(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    thread = models.ForeignKey(Thread, related_name='+')
    post = models.ForeignKey(Post, related_name='+')
    
    
class Edit(models.Model):
    forum = models.ForeignKey(Forum, related_name='+')
    thread = models.ForeignKey(Thread, related_name='+')
    post = models.ForeignKey(Post, related_name='+')    