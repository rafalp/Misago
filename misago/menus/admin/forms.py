from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ...admin.forms import YesNoSwitch
from ..models import MenuLink


class MenuLinkForm(forms.ModelForm):
    link = forms.URLField(
        label=_("Link"),
        help_text=_(
            "URL where the link should point to."
        ),
        required=True,
    )
    title = forms.CharField(
        label=_("Title"),
        help_text=_("Title that will be used"),
        required=True,
    )
    position = forms.ChoiceField(label=_("Position"), choices=MenuLink.LINK_POSITION_CHOICES)

    class Meta:
        model = MenuLink
        fields = ["link", "title", "position", "relevance"]

    def save(self):
        link = super().save()
        MenuLink.objects.invalidate_cache()
        return link


class FilterMenuLinksForm(forms.Form):
    position = forms.ChoiceField(
        label=_("Position"),
        required=False,
        choices=[("", _("All types"))] + MenuLink.LINK_POSITION_CHOICES,
    )
    content = forms.CharField(label=_("Content"), required=False)

    def filter_queryset(self, criteria, queryset):
        if criteria.get("position") is not None:
            queryset = queryset.filter(type=criteria["position"])

        if criteria.get("content"):
            search_title = Q(title__icontains=criteria["content"])
            search_link = Q(link__icontains=criteria["content"])
            queryset = queryset.filter(search_title | search_link)

        return queryset
