from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class PruningPolicy(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)
    posts = models.PositiveIntegerField(default=0)
    registered = models.PositiveIntegerField(default=0)
    last_visit = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'misago'

    def clean(self):
        if not (self.email and self.posts and self.registered and self.last_visit):
            raise ValidationError(_("Pruning policy must have at least one pruning criteria set to be valid."))

    def make_queryset(self):
        from misago.models import User
        queryset = User.objects

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
                    queryset = queryset.filter(qs)
            else:
                queryset = queryset.filter(email__iendswith=self.email)

        if self.posts:
            queryset = queryset.filter(posts__lt=self.posts)

        if self.registered:
            date = timezone.now() - timedelta(days=self.registered)
            queryset = queryset.filter(join_date__gte=date)

        if self.last_visit:
            date = timezone.now() - timedelta(days=self.last_visit)
            queryset = queryset.filter(last_date__gte=date)

        return queryset
