from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Forum(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    type = models.CharField(max_length=12)
    token = models.CharField(max_length=255,null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    description_preparsed = models.TextField(null=True, blank=True)
    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    #last_thread = models.ForeignKey('threads.Thread', related_name='+', null=True, blank=True)
    last_thread_name = models.CharField(max_length=255, null=True, blank=True)
    last_thread_slug = models.SlugField(null=True, blank=True)
    last_thread_date = models.DateTimeField(null=True, blank=True)
    last_poster = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_poster_style = models.CharField(max_length=255, null=True, blank=True)
    prune_start = models.PositiveIntegerField(default=0)
    prune_last = models.PositiveIntegerField(default=0)
    redirect = models.CharField(max_length=255, null=True, blank=True)
    style = models.CharField(max_length=255, null=True, blank=True)
    template = models.CharField(max_length=255, null=True, blank=True)
    closed = models.BooleanField(default=False)
    
    def __unicode__(self):
        if self.token == 'root':
           return unicode(_('Root Category')) 
        return unicode(self.name)
    
    def set_description(self, description):
        self.description = description.strip()
        self.description_preparsed = ''
        if self.description:
            import markdown
            self.description_preparsed = markdown.markdown(description, safe_mode='escape', output_format=settings.OUTPUT_FORMAT)
        
    def move_content(self, target):
        pass
    
    def prune(self):
        pass