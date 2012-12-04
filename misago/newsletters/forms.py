from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form, YesNoSwitch
from misago.ranks.models import Rank

class NewsletterForm(Form):
    name = forms.CharField(max_length=255)
    step_size = forms.IntegerField(initial=300,min_value=1)
    content_html = forms.CharField(widget=forms.Textarea)
    content_plain = forms.CharField(widget=forms.Textarea)
    ignore_subscriptions = forms.BooleanField(widget=YesNoSwitch,required=False) 
    ranks = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Rank.objects.order_by('name').all(),required=False)
    
    layout = (
              (
               _("Newsletter Options"),
               (
                ('name', {'label': _("Newsletter Name"), 'help_text': _("Newsletter name will be used as message subject in e-mails sent to members.")}),
                ('step_size', {'label': _("Step Size"), 'help_text': _("Number of users that message will be sent to before forum refreshes page displaying sending progress.")}),
                ('ranks', {'label': _("Limit to roles"), 'help_text': _("You can limit this newsletter only to members who have specific ranks. If you dont set any ranks, this newsletter will be sent to every user.")}),
                ('ignore_subscriptions', {'label': _("Ignore members preferences"), 'help_text': _("Change this option to yes if you want to send this newsletter to members that don't want to receive newsletters. This is good for emergencies.")}),
               )
              ),
              (
               _("Message"),
               (
                ('content_html', {'label': _("HTML Message"), 'help_text': _("HTML message visible to members who can read HTML e-mails."), 'attrs': {'rows': 10}}),
                ('content_plain', {'label': _("Plain Text Message"), 'help_text': _("Alternative plain text message that will be visible to members that can't or dont want to read HTML e-mails."), 'attrs': {'rows': 10}}),
               )
              ),
             )


class SearchNewslettersForm(Form):    
    name = forms.CharField(max_length=255, required=False)
    contains = forms.CharField(max_length=255, required=False)
    type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(('0', _("Only to subscribers")), ('1', _("To every member"))), required=False)
    rank = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Rank.objects.order_by('order').all(), required=False)
    
    layout = (
              (
               _("Search Newsletters"),
               (
                ('name', {'label': _("Newsletter Name"), 'attrs': {'placeholder': _("Name contains...")}}),
                ('contains', {'label': _("Message Contents"), 'attrs': {'placeholder': _("Message contains...")}}),
                ('type', {'label': _("Newsletter Type")}),
                ('rank', {'label': _("Recipient Rank")}),
               ),
              ),
             )