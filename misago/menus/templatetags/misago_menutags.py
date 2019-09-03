from django import template
from django.utils.translation import gettext as _
from django.utils.translation import ngettext
from ..models import MenuLink

register = template.Library()


@register.inclusion_tag('misago/menus/menu_links_tag.html', takes_context=False)
def top_menu_links():
    return {
        'links': MenuLink.objects.get_top_menu_links()
    }


@register.inclusion_tag('misago/menus/menu_links_tag.html', takes_context=False)
def footer_menu_links():
    return {
        'links': MenuLink.objects.filter(position='footer')
    }
