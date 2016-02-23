from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.categories.forms import AdminCategoryMultipleChoiceField

from misago.threads.models import Label


class LabelForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Label name"), validators=[validate_sluggable()])
    css_class = forms.CharField(
        label=_("CSS class"), required=False,
        help_text=_("Optional CSS clas used to style this label."))
    categories = AdminCategoryMultipleChoiceField(
        label=_('Categories'), required=False, include_root=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text=_('Select categories this label will be available in.'))

    class Meta:
        model = Label
        fields = ['name', 'css_class', 'categories']

    def clean_name(self):
        data = self.cleaned_data['name']
        self.instance.set_name(data)
        return data
