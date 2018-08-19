from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .models import Agreement
from .utils import set_agreement_as_active


class AgreementForm(forms.ModelForm):
    type = forms.ChoiceField(label=_("Type"), choices=Agreement.TYPE_CHOICES)
    title = forms.CharField(
        label=_("Title"),
        help_text=_("Optional, leave empty for agreement to be named after its type."),
        required=False,
    )
    is_active = forms.BooleanField(
        label=_("Set as active for its type"),
        help_text=_(
            "If other agreement is already active for this type, it will be unset and replaced "
            "with this one. "
            "Misago will ask users who didn't accept this agreement to do so before allowing them "
            "to continue using the site's features."
        ),
        required=False,
    )
    link = forms.URLField(
        label=_("Link"),
        help_text=_("If your agreement is located on other page, enter here a link to it."),
        required=False,
    )
    text = forms.CharField(
        label=_("Text"),
        help_text=_("You can use Markdown syntax for rich text elements."),
        widget=forms.Textarea,
        required=False,
    )

    class Meta:
        model = Agreement
        fields = ['type', 'title', 'link', 'text', 'is_active']

    def clean(self):
        data = super(AgreementForm, self).clean()

        if not data.get('link') and not data.get('text'):
            raise forms.ValidationError(_("Please fill in agreement link or text."))

        return data

    def save(self):
        agreement = super(AgreementForm, self).save()
        if agreement.is_active:
            set_agreement_as_active(agreement)
        Agreement.objects.invalidate_cache()
        return agreement


class SearchAgreementsForm(forms.Form):
    type = forms.MultipleChoiceField(
        label=_("Type"),
        required=False,
        choices=Agreement.TYPE_CHOICES,
    )
    content = forms.CharField(
        label=_("Content"),
        required=False,
    )

    def filter_queryset(self, search_criteria, queryset):
        criteria = search_criteria
        if criteria.get('type') is not None:
            queryset = queryset.filter(type__in=criteria['type'])

        if criteria.get('content'):
            search_title = Q(title__icontains=criteria['content'])
            search_text = Q(text__icontains=criteria['content'])
            queryset = queryset.filter(search_title | search_text)

        return queryset
