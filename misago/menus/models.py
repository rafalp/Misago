from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.db.models import Q

CACHE_KEY = "misago_menulinks"


class MenuLinkManager(models.Manager):
    def invalidate_cache(self):
        cache.delete(CACHE_KEY)

    def get_top_menu_links(self):
        return self.get_links().get(MenuLink.POSITION_TOP)

    def get_footer_menu_links(self):
        return self.get_links().get(MenuLink.POSITION_FOOTER)

    def get_links(self):
        links = self.get_links_from_cache()
        if links == "nada":
            links = self.get_links_from_db()
            cache.set(CACHE_KEY, links)
        return links

    def get_links_from_cache(self):
        return cache.get(CACHE_KEY, "nada")

    def get_footer_menu_links_from_db(self):
        return self.filter(
            Q(position=MenuLink.POSITION_TOP) | Q(position=MenuLink.POSITION_BOTH)
        ).values()

    def get_top_menu_links_from_db(self):
        return self.filter(
            Q(position=MenuLink.POSITION_FOOTER) | Q(position=MenuLink.POSITION_BOTH)
        ).values()

    def get_links_from_db(self):
        links = {
            MenuLink.POSITION_TOP: self.get_footer_menu_links_from_db(),
            MenuLink.POSITION_FOOTER: self.get_top_menu_links_from_db(),
        }
        return links


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
