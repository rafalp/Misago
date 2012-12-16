from django.db import models
       
class Session(models.Model):
    id = models.CharField(max_length=42, primary_key=True)
    data = models.TextField(db_column="session_data")
    user = models.ForeignKey('users.User', related_name='sessions', null=True, on_delete=models.SET_NULL)
    crawler = models.CharField(max_length=255, blank=True, null=True)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    start = models.DateTimeField()
    last = models.DateTimeField()
    team = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    matched = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

class Token(models.Model):
    id = models.CharField(max_length=42, primary_key=True)
    user = models.ForeignKey('users.User', related_name='signin_tokens')
    created = models.DateTimeField()
    accessed = models.DateTimeField()