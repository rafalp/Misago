from django.db import models
from misago.security import get_random_string

class Newsletter(models.Model):
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=32)
    step_size = models.PositiveIntegerField(default=0)
    progress = models.PositiveIntegerField(default=0)
    content_html = models.TextField(null=True,blank=True)
    content_plain = models.TextField(null=True,blank=True)
    ignore_subscriptions = models.BooleanField(default=False)
    ranks = models.ManyToManyField('ranks.Rank')
    
    def generate_token(self):
        self.token = get_random_string(32)
    
    def parse_name(self, tokens):
        name = self.name
        for key in tokens:
            name = name.replace(key, tokens[key])
        return name
    
    def parse_html(self, tokens):
        content_html = self.content_html
        for key in tokens:
            content_html = content_html.replace(key, tokens[key])
        return content_html
    
    def parse_plain(self, tokens):
        content_plain = self.content_plain
        for key in tokens:
            content_plain = content_plain.replace(key, tokens[key])
        return content_plain