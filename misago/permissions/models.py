from django.conf import settings
from django.db import models


class CategoryPermission(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    group = models.ForeignKey("misago_users.Group", on_delete=models.CASCADE)
    permission = models.CharField(max_length=32)


class CategoryModerator(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    group = models.ForeignKey("misago_users.Group", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )
