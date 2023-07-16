from django import forms
from django.utils.translation import pgettext_lazy

from ...admin.forms import YesNoSwitch
from ..models import MenuItem
from ..cache import clear_menus_cache


class MenuItemForm(forms.ModelForm):
    title = forms.CharField(label=pgettext_lazy("admin menu item form", "Title"))
    url = forms.URLField(
        label=pgettext_lazy("admin menu item form", "URL"),
        help_text=pgettext_lazy(
            "admin menu item form", "URL where this item will point to."
        ),
    )
    menu = forms.ChoiceField(
        label=pgettext_lazy("admin menu item form", "Menu"),
        choices=MenuItem.MENU_CHOICES,
        help_text=pgettext_lazy(
            "admin menu item form", "Menu in which this item will be displayed."
        ),
    )
    css_class = forms.CharField(
        label=pgettext_lazy("admin menu item form", "CSS class"),
        help_text=pgettext_lazy(
            "admin menu item form",
            'Optional. Additional CSS class to include in link\'s "class" HTML attribute.',
        ),
        required=False,
    )
    target_blank = YesNoSwitch(
        label=pgettext_lazy("admin menu item form", "Open this link in new window"),
        help_text=pgettext_lazy(
            "admin menu item form",
            'Enabling this option will result in the target="_blank" attribute being added to this link\'s HTML element.',
        ),
        required=False,
    )
    rel = forms.CharField(
        label=pgettext_lazy("admin menu item form", "Rel attribute"),
        help_text=pgettext_lazy(
            "admin menu item form",
            'Optional "rel" attribute that this item will use (ex. "nofollow").',
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
