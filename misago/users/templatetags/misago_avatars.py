from django import template
from django.templatetags.static import static

from ...conf import settings
from ..avatars.selection import resolve_avatar_for_size

register = template.Library()


@register.filter(name="avatar")
def avatar(user, size=200):
    avatars = getattr(user, "avatars", None) if user else None
    found_avatar = resolve_avatar_for_size(avatars, size)
    if not found_avatar:
        return static(settings.MISAGO_BLANK_AVATAR)

    return found_avatar["url"]
