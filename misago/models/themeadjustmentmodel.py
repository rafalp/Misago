from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

class ThemeAdjustment(models.Model):
    theme = models.CharField(max_length=255, unique=True,
                             error_messages={'unique': _("User agents for this theme are already defined.")})
    useragents = models.TextField(null=True, blank=True)
    
    class Meta:
        app_label = 'misago'

    def adjust_theme(self, useragent):
        for string in self.useragents.splitlines():
            if string in useragent:
                return True
        return False
    
    def save(self, *args, **kwargs):
        cache.delete('client_adjustments')
        super(ThemeAdjustment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete('client_adjustments')
        super(ThemeAdjustment, self).delete(*args, **kwargs)