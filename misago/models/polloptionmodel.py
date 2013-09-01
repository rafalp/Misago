from django.db import models

class PollOption(models.Model):
    poll = models.ForeignKey('Poll', related_name="option_set")
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    name = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'misago'