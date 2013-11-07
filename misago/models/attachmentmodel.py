from django.db import models

class Attachment(object):#models.Model):
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        app_label = 'misago'