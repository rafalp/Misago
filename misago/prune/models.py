from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.users.models import User

class Policy(models.Model):
    """
    Pruning policy
    """
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,null=True,blank=True)
    posts = models.PositiveIntegerField(default=0)
    registered = models.PositiveIntegerField(default=0)
    last_visit = models.PositiveIntegerField(default=0)
    
    def clean(self):
        if not (self.email and self.posts and self.registered and self.last_visit):
            raise ValidationError(_("Pruning policy must have at least one pruning criteria set to be valid."))
        
    def get_model(self):
        model = User.objects
        
        if self.email:
            if ',' in self.email:
                qs = None
                for name in self.email.split(','):
                    name = name.strip().lower()
                    if name:
                        if qs:
                            qs = qs | Q(email__iendswith=name)
                        else:
                            qs = Q(email__iendswith=name)
                if qs:
                    model = model.filter(qs)
            else:
                model = model.filter(email__iendswith=self.email)
                
        if self.posts:
            model = model.filter(posts__lt=self.posts)
            
        if self.registered:
            date = timezone.now() - timedelta(days=self.registered)
            model = model.filter(join_date__gte=date)
            
        if self.last_visit:
            date = timezone.now() - timedelta(days=self.last_visit)
            model = model.filter(last_date__gte=date)
            
        return model