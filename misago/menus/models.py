from django.db import models
from django.utils.translation import pgettext_lazy


class MenuItem(models.Model):
    MENU_BOTH = "both"
    MENU_NAVBAR = "navbar"
    MENU_FOOTER = "footer"
    MENU_CHOICES = [
        (MENU_BOTH, pgettext_lazy("menu choice", "Navbar and footer")),
        (MENU_NAVBAR, pgettext_lazy("menu choice", "Navbar")),
        (MENU_FOOTER, pgettext_lazy("menu choice", "Footer")),
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
