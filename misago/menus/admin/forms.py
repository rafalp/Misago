from django import forms
from django.utils.translation import gettext_lazy as _

from ...admin.forms import YesNoSwitch
from ..models import MenuItem
from ..cache import clear_menus_cache


class MenuItemForm(forms.ModelForm):
    title = forms.CharField(label=_("Title"))
    url = forms.URLField(
        label=_("URL"), help_text=_("URL where this item will point to.")
    )
    menu = forms.ChoiceField(
        label=_("Menu"),
        choices=MenuItem.MENU_CHOICES,
        help_text=_("Menu in which this item will be displayed."),
    )
    css_class = forms.CharField(
        label=_("CSS class"),
        help_text=_('If you want to set custom value for link\'s "class".'),
        required=False,
    )
    target_blank = YesNoSwitch(
        label=_("Open this link in new window"),
        help_text=_(
            'Enabling this option will result in the target="_blank" attribute being '
            "added to this link's HTML element."
        ),
        required=False,
    )
    rel = forms.CharField(
        label=_("Rel attribute"),
        help_text=_(
            'Optional "rel" attribute that this item will use (ex. "nofollow").'
        ),
        required=False,
    )

    class Meta:
        model = MenuItem
        fields = ["title", "url", "menu", "css_class", "target_blank", "rel"]

    def save(self):
        item = super().save()
        clear_menus_cache()
        return item
