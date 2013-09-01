from django.db import models

class PollVote(models.Model):
    poll = models.ForeignKey('Poll')
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    option = models.ForeignKey('PollOption')
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)

    class Meta:
        app_label = 'misago'