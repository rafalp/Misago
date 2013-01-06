from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.utils import slugify

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
    merges = models.PositiveIntegerField(default=0,db_index=True)
    score = models.PositiveIntegerField(default=30,db_index=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    start = models.DateTimeField(db_index=True)
    start_post = models.ForeignKey('Post',related_name='+',null=True,blank=True,on_delete=models.SET_NULL)
    start_poster = models.ForeignKey('users.User',null=True,blank=True)
    start_poster_name = models.CharField(max_length=255)
    start_poster_slug = models.SlugField(max_length=255)
    start_poster_style = models.CharField(max_length=255,null=True,blank=True)
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
    
    def sync(self):
        # Counters
        self.replies = self.post_set.filter(moderated=False).filter(deleted=False).count() - 1
        if self.replies < 0:
            self.replies = 0
        self.replies_reported = self.post_set.filter(reported=True).count()
        self.replies_moderated = self.post_set.filter(moderated=True).count()
        self.replies_deleted = self.post_set.filter(deleted=True).count()
        # First post
        start_post = self.post_set.order_by('merge', 'id')[0:][0]
        self.start = start_post.date
        self.start_post = start_post
        self.start_poster = start_post.user
        self.start_poster_name = start_post.user_name
        self.start_poster_slug = slugify(start_post.user_name)
        self.start_poster_style = start_post.user.rank.style if start_post.user else ''
        self.upvotes = start_post.upvotes
        self.downvotes = start_post.downvotes
        # Last post
        if self.replies > 0:
            last_post = self.post_set.order_by('-merge', '-id').filter(moderated=False).filter(deleted=False)[0:][0]
        else:
            last_post = start_post
        self.last = last_post.date
        self.last_post = last_post
        self.last_poster = last_post.user
        self.last_poster_name = last_post.user_name
        self.last_poster_slug = slugify(last_post.user_name)
        self.last_poster_style = last_post.user.rank.style if last_post.user else ''
        # Flags
        self.moderated = start_post.moderated
        self.deleted = start_post.deleted
        self.merges = last_post.merge
    

class PostManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(date__gte=start).filter(date__lte=end)
    

class Post(models.Model):
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey(Thread)
    merge = models.PositiveIntegerField(default=0,db_index=True)
    user = models.ForeignKey('users.User',null=True,blank=True)
    user_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    post = models.TextField()
    post_preparsed = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()
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
    
    def set_checkpoint(self, request, action):
        if request.user.is_authenticated():
            self.checkpoint_set.create(
                                       forum=self.forum,
                                       thread=self.thread,
                                       post=self,
                                       action=action,
                                       user=request.user,
                                       user_name=request.user.username,
                                       user_slug=request.user.username_slug,
                                       date=timezone.now(),
                                       ip=request.session.get_ip(request),
                                       agent=request.META.get('HTTP_USER_AGENT'),
                                       )


class Change(models.Model):
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey(Thread)
    post = models.ForeignKey(Post)
    user = models.ForeignKey('users.User',null=True,blank=True)
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    reason = models.CharField(max_length=255,null=True,blank=True)
    thread_name_new = models.CharField(max_length=255,null=True,blank=True)
    thread_name_old = models.CharField(max_length=255,null=True,blank=True)
    post_content = models.TextField()
    size = models.IntegerField(default=0)
    change = models.IntegerField(default=0)


class Checkpoint(models.Model):
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey(Thread)
    post = models.ForeignKey(Post)
    action = models.CharField(max_length=255)
    user = models.ForeignKey('users.User',null=True,blank=True)
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    