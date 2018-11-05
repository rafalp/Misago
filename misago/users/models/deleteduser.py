from django.db import models


DELETED_BY = (
    (1, 'By User'),
    (2, 'By Staff'),
    (3, 'By System'),
)


class DeletedUser(models.Model):
    deleted_on = models.DateTimeField(default=timezone.now)
    deleted_by = models.PositiveIntegerField(
        choices=DELETED_BY,
        default=1
    )
    
    class Meta:
        get_latest_by = "deleted_on"
