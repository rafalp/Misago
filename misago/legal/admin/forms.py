from django import forms
from django.db.models import Q
from django.utils.translation import pgettext_lazy

from ...admin.forms import YesNoSwitch
from ..models import Agreement
from .utils import disable_agreement, set_agreement_as_active


class AgreementForm(forms.ModelForm):
    type = forms.ChoiceField(
        label=pgettext_lazy("admin agreement form", "Type"),
        choices=Agreement.TYPE_CHOICES,
    )
    title = forms.CharField(
        label=pgettext_lazy("admin agreement form", "Title"),
        help_text=pgettext_lazy(
            "admin agreement form",
            "Optional, leave empty for agreement to be named after its type.",
        ),
        required=False,
    )
    is_active = YesNoSwitch(
        label=pgettext_lazy("admin agreement form", "Active for its type"),
        help_text=pgettext_lazy(
            "admin agreement form",
            "If other agreement is already active for this type, it will be unset and replaced with this one. Misago will ask users who didn't accept this agreement to do so before allowing them to continue using the site.",
        ),
    )
    link = forms.URLField(
        label=pgettext_lazy("admin agreement form", "Link"),
        help_text=pgettext_lazy(
            "admin agreement form",
            "If your agreement is located on other page, enter here a link to it.",
        ),
        required=False,
    )
    text = forms.CharField(
        label=pgettext_lazy("admin agreement form", "Text"),
        help_text=pgettext_lazy(
            "admin agreement form",
            "You can use Markdown syntax for rich text elements.",
        ),
        widget=forms.Textarea,
        required=False,
    )

    class Meta:
        model = Agreement
        fields = ["type", "title", "link", "text", "is_active"]

    def clean(self):
        data = super().clean()

        if not data.get("link") and not data.get("text"):
            raise forms.ValidationError(
                pgettext_lazy(
                    "admin agreement form", "Please fill in agreement link or text."
                )
            )

        return data

    def save(self):
        agreement = super().save()
        if agreement.is_active:
            set_agreement_as_active(agreement)
        else:
            disable_agreement(agreement)
        Agreement.objects.invalidate_cache()
        return agreement


class FilterAgreementsForm(forms.Form):
    type = forms.ChoiceField(
        label=pgettext_lazy("admin agreement form", "Type"),
        required=False,
        choices=[("", pgettext_lazy("admin agreement type field choice", "All types"))]
        + Agreement.TYPE_CHOICES,
    )
    content = forms.CharField(
        label=pgettext_lazy("admin agreement form", "Content"), required=False
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("type") is not None:
            queryset = queryset.filter(type=criteria["type"])

        if criteria.get("content"):
            search_title = Q(title__icontains=criteria["content"])
            search_text = Q(text__icontains=criteria["content"])
            queryset = queryset.filter(search_title | search_text)

        return queryset
