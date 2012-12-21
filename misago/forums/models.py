from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel,TreeForeignKey
from misago.roles.models import Role

class ForumManager(models.Manager):
    def treelist(self, acl, parent=None):
        complete_list = []
        forums_list = []
        parents = {}
        
        if parent:
            queryset = Forum.objects.filter(pk__in=acl.known_forums).filter(lft__gt=parent.lft).filter(rght__lt=parent.rght).order_by('lft')
        else:
            queryset = Forum.objects.filter(pk__in=acl.known_forums).order_by('lft')
            
        for forum in queryset:
            forum.subforums = []
            parents[forum.pk] = forum
            complete_list.append(forum)
            if forum.parent_id in parents:
                parents[forum.parent_id].subforums.append(forum)
            else:
                forums_list.append(forum)
        
        # Second iteration - sum up forum counters
        for forum in reversed(complete_list):
            if forum.parent_id in parents and parents[forum.parent_id].type != 'redirect':
                parents[forum.parent_id].threads += forum.threads
                parents[forum.parent_id].threads_delta += forum.threads_delta
                parents[forum.parent_id].posts += forum.posts
                parents[forum.parent_id].posts_delta += forum.posts_delta
                if acl.can_browse(forum.pk) and forum.last_thread_date and (not parents[forum.parent_id].last_thread_date or forum.last_thread_date > parents[forum.parent_id].last_thread_date):
                    parents[forum.parent_id].last_thread = forum.last_thread
                    parents[forum.parent_id].last_thread_name = forum.last_thread_name
                    parents[forum.parent_id].last_thread_slug = forum.last_thread_slug
                    parents[forum.parent_id].last_thread_date = forum.last_thread_date
                    parents[forum.parent_id].last_poster = forum.last_poster
                    parents[forum.parent_id].last_poster_name = forum.last_poster_name
                    parents[forum.parent_id].last_poster_slug = forum.last_poster_slug
                    parents[forum.parent_id].last_poster_style = forum.last_poster_style
        return forums_list


class Forum(MPTTModel):
    parent = TreeForeignKey('self',null=True,blank=True,related_name='children')
    type = models.CharField(max_length=12)
    token = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True,blank=True)
    description_preparsed = models.TextField(null=True,blank=True)
    threads = models.PositiveIntegerField(default=0)
    threads_delta = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    posts_delta = models.IntegerField(default=0)
    redirects = models.PositiveIntegerField(default=0)
    redirects_delta = models.IntegerField(default=0)
    last_thread = models.ForeignKey('threads.Thread',related_name='+',null=True,blank=True,on_delete=models.SET_NULL)
    last_thread_name = models.CharField(max_length=255,null=True,blank=True)
    last_thread_slug = models.SlugField(null=True,blank=True)
    last_thread_date = models.DateTimeField(null=True,blank=True)
    last_poster = models.ForeignKey('users.User',related_name='+',null=True,blank=True,on_delete=models.SET_NULL)
    last_poster_name = models.CharField(max_length=255,null=True,blank=True)
    last_poster_slug = models.SlugField(max_length=255,null=True,blank=True)
    last_poster_style = models.CharField(max_length=255,null=True,blank=True)
    prune_start = models.PositiveIntegerField(default=0)
    prune_last = models.PositiveIntegerField(default=0)
    redirect = models.CharField(max_length=255,null=True,blank=True)
    style = models.CharField(max_length=255,null=True,blank=True)
    closed = models.BooleanField(default=False)
    
    objects = ForumManager()   
    
    def __unicode__(self):
        if self.token == 'root':
           return unicode(_('Root Category')) 
        return unicode(self.name)
    
    def set_description(self, description):
        self.description = description.strip()
        self.description_preparsed = ''
        if self.description:
            import markdown
            self.description_preparsed = markdown.markdown(description,safe_mode='escape',output_format=settings.OUTPUT_FORMAT)
       
    def copy_permissions(self, target):
        if target.pk != self.pk:
            for role in Role.objects.all():
                perms = role.get_permissions()
                try:
                    perms['forums'][self.pk] = perms['forums'][target.pk]
                    role.set_permissions(perms)
                    role.save(force_update=True)
                except KeyError:
                    pass
        
    def move_content(self, target):
        pass
    
    def prune(self):
        pass