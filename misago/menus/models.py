from django.db import models
from django.utils.translation import gettext_lazy as _


class MenuItem(models.Model):
    MENU_BOTH = "both"
    MENU_NAVBAR = "navbar"
    MENU_FOOTER = "footer"
    MENU_CHOICES = [
        (MENU_BOTH, _("Navbar and footer")),
        (MENU_NAVBAR, _("Navbar")),
        (MENU_FOOTER, _("Footer")),
    ]

    menu = models.CharField(max_length=6, choices=MENU_CHOICES)
    title = models.CharField(max_length=255)
    url = models.URLField()
    order = models.IntegerField(default=0)
    css_class = models.CharField(max_length=255, null=True, blank=True)
    target_blank = models.BooleanField(default=False)
    rel = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("order",)
        get_latest_by = "order"

    def __str__(self):
        return self.title
