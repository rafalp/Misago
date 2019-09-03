from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.core.cache import cache

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

    def get_links_from_db(self):
        links = {MenuLink.POSITION_TOP: [], MenuLink.POSITION_FOOTER: []}
        for link in MenuLink.objects.all():
            links[link.position].append(
                {
                    "id": link.id,
                    "title": link.title,
                    "link": link.link,
                    "relevance": link.relevance,
                }
            )
        return links


class MenuLink(models.Model):
    POSITION_TOP = "top"
    POSITION_FOOTER = "footer"
    LINK_POSITION_CHOICES = [
        (POSITION_TOP, _("Top navbar")),
        (POSITION_FOOTER, _("Footer")),
    ]

    link = models.URLField()
    title = models.CharField(max_length=150)
    position = models.CharField(max_length=20, choices=LINK_POSITION_CHOICES)
    relevance = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(1000)],
        default=500,
        help_text=_("Relevance that the link has, used for ordering. (Max: 1000)"),
    )
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    created_by_name = models.CharField(max_length=255, null=True, blank=True)
    last_modified_on = models.DateTimeField(null=True, blank=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    last_modified_by_name = models.CharField(max_length=255, null=True, blank=True)

    objects = MenuLinkManager()

    class Meta:
        unique_together = ("link", "position")
        ordering = ("-relevance",)

    def __str__(self):
        return self.link

    def set_created_by(self, user):
        self.created_by = user
        self.created_by_name = user.username

    def set_last_modified_by(self, user):
        self.last_modified_by = user
        self.last_modified_by_name = user.username
