from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form, YesNoSwitch

class PruningForm(Form):
    name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255,required=False)
    posts = forms.IntegerField(min_value=0,initial=0)
    registered = forms.IntegerField(min_value=0,initial=0)
    last_visit = forms.IntegerField(min_value=0,initial=0)
    
    layout = (
              (
               _("Basic Policy Options"),
               (
                ('name', {'label': _("Policy Name"), 'help_text': _("Short, describtive name of this pruning policy.")}),
               )
              ),
              (
               _("Pruning Policy Criteria"),
               (
                ('email', {'label': _("Member E-mail Address ends with"), 'help_text': _("If you want to, you can enter more than one e-mail suffix by separating them with comma.")}),
                ('posts', {'label': _("Member has no more posts than"), 'help_text': _("Maximum number of posts member is allowed to have to fall under policy. For example if you enter in 10 posts and make this only criteria, every user that has less than 10 posts will be deleted. Enter zero to dont use this criteria")}),
                ('registered', {'label': _("User is member for no more than"), 'help_text': _("Maximal number of days user is member for. For exmaple if you enter in 15 days and make this only criteria, every user who is member for less than 15 days will be deleted. Enter zero to dont use this criteria.")}),
                ('last_visit', {'label': _("User last visit was before"), 'help_text': _("Maximal allowed inactivity period in days. For example if you enter in 300 days and make this only criteria for deleting users, every member who did not signed into forums in last 300 days will be deleted. Enter zero to dont use this criteria.")}),
               )
              ),
             )
    