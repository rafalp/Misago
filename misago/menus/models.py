from django.db import models
from django.utils.translation import gettext_lazy as _


class MenuLinkManager(models.Manager):
    pass


class MenuLink(models.Model):
    POSITION_TOP = "top"
    POSITION_FOOTER = "footer"
    POSITION_BOTH = "both"
    LINK_POSITION_CHOICES = [
        (POSITION_TOP, _("Header navbar")),
        (POSITION_FOOTER, _("Footer")),
        (POSITION_BOTH, _("Header and footer")),
    ]

    link = models.URLField()
    title = models.CharField(max_length=150)
    position = models.CharField(max_length=20, choices=LINK_POSITION_CHOICES)
    order = models.IntegerField(default=0)
    css_class = models.CharField(max_length=255, null=True, blank=True)
    target = models.CharField(max_length=100, null=True, blank=True)
    rel = models.CharField(max_length=100, null=True, blank=True)

    objects = MenuLinkManager()

    class Meta:
        unique_together = ("link", "position")
        ordering = ("order",)
        get_latest_by = "order"

    def __str__(self):
        return self.link
