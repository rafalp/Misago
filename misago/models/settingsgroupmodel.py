from django.db import models

class SettingsGroup(models.Model):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'misago'

    def is_active(self, active_group):
        try:
            return self.pk == active_group.pk
        except AttributeError:
            return False