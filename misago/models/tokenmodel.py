from django.db import models

class Token(models.Model):
    id = models.CharField(max_length=42, primary_key=True)
    user = models.ForeignKey('User', related_name='signin_tokens')
    created = models.DateTimeField()
    accessed = models.DateTimeField()

    class Meta:
        app_label = 'misago'