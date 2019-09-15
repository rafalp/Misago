from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import MenuLink
from ..cache import clear_menus_cache


class MenuLinkForm(forms.ModelForm):
    link = forms.URLField(
        label=_("Link"),
        help_text=_("URL where the link should point to."),
        required=True,
    )
    title = forms.CharField(
        label=_("Title"), help_text=_("Title that will be used"), required=True
    )
    position = forms.ChoiceField(
        label=_("Position"),
        choices=MenuLink.LINK_POSITION_CHOICES,
        help_text=_("Position/s the link should be located"),
    )
    css_class = forms.CharField(
        label=_("CSS Class"),
        help_text=_(
            "Optional CSS class used to customize this link appearance in templates."
        ),
        required=False,
    )
    target = forms.CharField(
        label=_("Target"),
        help_text=_(
            "Optional target attribute that this link will use (ex. '_blank')."
        ),
        required=False,
    )
    rel = forms.CharField(
        label=_("Rel"),
        help_text=_("Optional rel attribute that this link will use (ex. 'nofollow')."),
        required=False,
    )

    class Meta:
        model = MenuLink
        fields = ["link", "title", "position", "css_class", "target", "rel"]

    def save(self):
        link = super().save()
        clear_menus_cache()
        return link
