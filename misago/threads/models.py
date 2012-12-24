from django.db import models
from django.utils.translation import ugettext_lazy as _

class ThreadManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(start__gte=start).filter(start__lte=end)


class Thread(models.Model):
    forum = models.ForeignKey('forums.Forum')
    weight = models.PositiveIntegerField(default=0,db_index=True)
    type = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField(default=0)
    replies_reported = models.PositiveIntegerField(default=0)
    replies_moderated = models.PositiveIntegerField(default=0)
    replies_deleted = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=30,db_index=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    start = models.DateTimeField(db_index=True)
    start_post = models.ForeignKey('Post',related_name='+',null=True,blank=True,on_delete=models.SET_NULL)
    start_poster = models.ForeignKey('users.User',null=True,blank=True)
    start_poster_name = models.CharField(max_length=255)
    start_poster_slug = models.SlugField(max_length=255)
    start_poster_style = models.CharField(max_length=255)
    last = models.DateTimeField(db_index=True)
    last_post = models.ForeignKey('Post',related_name='+',null=True,blank=True,on_delete=models.SET_NULL)
    last_poster = models.ForeignKey('users.User',related_name='+',null=True,blank=True)
    last_poster_name = models.CharField(max_length=255,null=True,blank=True)
    last_poster_slug = models.SlugField(max_length=255,null=True,blank=True)
    last_poster_style = models.CharField(max_length=255,null=True,blank=True)
    moderated = models.BooleanField(default=False,db_index=True)
    deleted = models.BooleanField(default=False,db_index=True)
    closed = models.BooleanField(default=False)
    
    objects = ThreadManager()
    
    statistics_name = _('New Threads')
        
    def get_date(self):
        return self.start
    

class PostManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(date__gte=start).filter(date__lte=end)
    

class Post(models.Model):
    forum = models.ForeignKey('forums.Forum',related_name='+')
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey('users.User',null=True,blank=True)
    user_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    post = models.TextField()
    post_preparsed = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
    edited = models.BooleanField(default=False)
    edits = models.PositiveIntegerField(default=0)
    edit_date = models.DateTimeField(null=True,blank=True)
    edit_reason = models.CharField(max_length=255,null=True,blank=True)
    edit_user = models.ForeignKey('users.User',related_name='+',null=True)
    edit_user_name = models.CharField(max_length=255,null=True,blank=True)
    edit_user_slug = models.SlugField(max_length=255,null=True,blank=True)
    reported = models.BooleanField(default=False)
    moderated = models.BooleanField(default=False,db_index=True)
    deleted = models.BooleanField(default=False,db_index=True)
    protected = models.BooleanField(default=False)
    
    objects = PostManager()
    
    statistics_name = _('New Posts')
    
    def get_date(self):
        return self.date