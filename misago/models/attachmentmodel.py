from django.db import models

class Attachment(models.Model):
    filetype = models.ForeignKey('AttachmentType')
    forum = models.ForeignKey('Forum', null=True, blank=True, on_delete=models.SET_NULL)
    thread = models.ForeignKey('Thread', null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey('Post', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255)
    user_name_slug = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    date = models.DateTimeField()
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    size = models.PositiveIntegerField(max_length=255)

    class Meta:
        app_label = 'misago'