from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form
from misago.themes.models import ThemeAdjustment
from misago.utils.validators import validate_sluggable

available_themes = []
for theme in settings.INSTALLED_THEMES[0:-1]:
    available_themes.append((theme, theme))


class ThemeAdjustmentForm(Form):
    theme = forms.ChoiceField(choices=available_themes, required=False)
    useragents = forms.CharField(widget=forms.Textarea, required=False)
    
    layout = (
              (
               _("Theme Adjustment"),
               (
                ('theme', {'label': _("Theme"), 'help_text': _("Select theme that is to replace default one.")}),
                ('useragents', {'label': _("UserAgent Strings"), 'help_text': _("Enter UserAgent strings for which selected theme has to replace default one. Each string has to be entered in new line. This is case insensitive")}),
                ),
               ),
              )

    def __init__(self, adjustment=None, *args, **kwargs):
        self.request = kwargs['request']
        if adjustment:
            self.adjustment = adjustment
        else:
            self.adjustment = ThemeAdjustment()
        super(ThemeAdjustmentForm, self).__init__(*args, **kwargs)
        
    def clean_theme(self):
        self.adjustment.theme = self.cleaned_data['theme']
        self.adjustment.full_clean()
        return self.cleaned_data['theme']

    def clean_useragents(self):
        agents_raw = self.cleaned_data['useragents'].strip().lower().splitlines()
        agents = []
        for line in agents_raw:
            line = line.strip()
            if line and not line in agents:
                agents.append(line)
        self.cleaned_data['useragents'] = agents
        if not agents:
            raise ValidationError(_("You have to enter at least one UserAgent."))
        return self.cleaned_data['useragents']
