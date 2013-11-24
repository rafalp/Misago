from django.db import models

class Session(models.Model):
    id = models.CharField(max_length=42, primary_key=True)
    data = models.TextField(db_column="session_data")
    user = models.ForeignKey('User', related_name='sessions', null=True, on_delete=models.SET_NULL)
    crawler = models.CharField(max_length=255, blank=True, null=True)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    start = models.DateTimeField()
    last = models.DateTimeField()
    team = models.BooleanField(default=False)
    rank = models.ForeignKey('Rank', related_name='sessions', null=True, on_delete=models.SET_NULL)
    admin = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)

    class Meta:
        app_label = 'misago'