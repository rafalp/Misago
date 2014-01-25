from datetime import timedelta
from django.utils import timezone as tz
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form

class GenerateStatisticsForm(Form):
    provider_model = forms.ChoiceField(label=_('Report Type'),
                                       help_text=_('Select statistics provider.'))
    date_start = forms.DateField(label=_('Time Period'),
                                 help_text=_('Enter start and end date for time period you want to take data from to use in graph.'),
                                 initial=tz.now() - timedelta(days=7))
    date_end = forms.DateField(initial=tz.now() + timedelta(days=1))
    stats_precision = forms.ChoiceField(label=_('Graph Precision'),
                                        choices=(('day', _('For each day')), ('week', _('For each week')), ('month', _('For each month')), ('year', _('For each year'))))

    def __init__(self, *args, **kwargs):
        provider_choices = kwargs.get('provider_choices')
        del kwargs['provider_choices']
        super(GenerateStatisticsForm, self).__init__(*args, **kwargs)
        self.fields['provider_model'] = forms.ChoiceField(choices=provider_choices)
