from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, YesNoSwitch
from misago.models import Rank
from misago.validators import validate_sluggable

class NewsletterForm(Form):
    name = forms.CharField(label=_("Newsletter Name"),
                           help_text=_("Newsletter name will be used as message subject in e-mails sent to members."),
                           max_length=255, validators=[validate_sluggable(
                                                                          _("Newsletter name must contain alphanumeric characters."),
                                                                          _("Newsletter name is too long.")
                                                                          )])
    step_size = forms.IntegerField(label=_("Step Size"),
                                   help_text=_("Number of users that message will be sent to before forum refreshes page displaying sending progress."),
                                   initial=300, min_value=1)
    content_html = forms.CharField(label=_("HTML Message"),
                                   help_text=_("HTML message visible to members who can read HTML e-mails."),
                                   widget=forms.Textarea)
    content_plain = forms.CharField(label=_("Plain Text Message"),
                                    help_text=_("Alternative plain text message that will be visible to members that can't or dont want to read HTML e-mails."),
                                    widget=forms.Textarea)
    ignore_subscriptions = forms.BooleanField(label=_("Ignore members preferences"),
                                              help_text=_("Change this option to yes if you want to send this newsletter to members that don't want to receive newsletters. This is good for emergencies."),
                                              widget=YesNoSwitch, required=False)
    ranks = forms.ModelMultipleChoiceField(label=_("Limit to roles"),
                                           help_text=_("You can limit this newsletter only to members who have specific ranks. If you dont set any ranks, this newsletter will be sent to every user."),
                                           widget=forms.CheckboxSelectMultiple, queryset=Rank.objects.order_by('name').all(), required=False)


class SearchNewslettersForm(Form):
    name = forms.CharField(label=_("Newsletter Name"),
                           max_length=255, required=False)
    contains = forms.CharField(label=_("Message Contents"),
                               max_length=255, required=False)
    type = forms.TypedMultipleChoiceField(label=_("Newsletter Type"),
                                          widget=forms.CheckboxSelectMultiple, choices=((0, _("Only to subscribers")), (1, _("To every member"))), coerce=int, required=False)
    rank = forms.ModelMultipleChoiceField(label=_("Recipient Rank"), widget=forms.CheckboxSelectMultiple, queryset=Rank.objects.order_by('order').all(), required=False)