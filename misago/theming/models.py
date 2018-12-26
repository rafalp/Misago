from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Theme(MPTTModel):
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ["is_default", "name"]

# class Css(models.Model):
#     theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="css")

#     name = models.CharField(max_length=255)
#     url = models.UrlField(max_length=255, null=True, blank=True)
#     file = models.ImageField(max_length=255, null=True, blank=True)
#     size = models.PositiveIntegerField()

#     order = models.IntegerField(default=0)
#     is_enabled = models.BooleanField(default=True)

#     uploaded_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)


# class Font(models.Model):
#     theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="fonts")

#     name = models.CharField(max_length=255)
#     file = models.FileField(max_length=255)
#     type = models.CharField(max_length=255)
#     size = models.PositiveIntegerField()

#     uploaded_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)


# class Image(models.Model):
#     theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="images")

#     name = models.CharField(max_length=255)
#     file = models.ImageField(max_length=255)
#     type = models.CharField(max_length=255)
#     width = models.PositiveIntegerField()
#     heigh = PositiveIntegerField()
#     size = models.PositiveIntegerField()

#     uploaded_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
