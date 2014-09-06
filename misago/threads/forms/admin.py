from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.forums.forms import ForumsMultipleChoiceField

from misago.threads.models import Label


class LabelForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Label name"), validators=[validate_sluggable()])
    css_class = forms.CharField(
        label=_("CSS class"), required=False,
        help_text=_("Optional CSS clas used to style this label."))
    forums = ForumsMultipleChoiceField(
        label=_('Forums'), required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text=_('Select forums this label will be available in.'))

    class Meta:
        model = Label
        fields = ['name', 'css_class', 'forums']

    def clean_name(self):
        data = self.cleaned_data['name']
        self.instance.set_name(data)
        return data
