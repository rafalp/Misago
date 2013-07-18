from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form

class BanForm(Form):
    """
    New/Edit Ban form
    """
    test = forms.TypedChoiceField(label=_("Ban Rule"),
    							  help_text=_("Select ban type from list and define rule by entering it in text field. If you want to ban specific user, enter here either his Username or E-mail address. If you want to define blanket ban, you can use wildcard (\"*\"). For example to forbid all members from using name suggesting that member is an admin, you can set ban that forbids \"Admin*\" as username."),
    							  choices=(
                                           (0, _('Ban Username and e-mail')),
                                           (1, _('Ban Username')),
                                           (2, _('Ban E-mail address')),
                                           (3, _('Ban IP Address'))
                                           ), coerce=int)
    reason_user = forms.CharField(label=_("User-visible Ban Message"),
    							  help_text=_("Optional Ban message that will be displayed to banned members."),
    							  widget=forms.Textarea, required=False)
    reason_admin = forms.CharField(label=_("Team-visible Ban Message"),
    							   help_text=_("Optional Ban message that will be displayed to forum team members."),
    							   widget=forms.Textarea, required=False)
    ban = forms.CharField(max_length=255)
    expires = forms.DateField(label=_("Ban Expiration"),
    						  help_text=_("If you want to, you can set this ban's expiration date by entering it here using YYYY-MM-DD format. Otherwhise you can leave this field empty making this ban permanent."),
    						  required=False)


class SearchBansForm(Form):
    ban = forms.CharField(label=_("Ban"), required=False)
    reason = forms.CharField(label=_("Messages"), required=False)
    test = forms.TypedMultipleChoiceField(label=_("Type"),
    									  widget=forms.CheckboxSelectMultiple,
    									  coerce=int, required=False,
    									  choices=(
                                           (0, _('Username and e-mail')),
                                           (1, _('Username')),
                                           (2, _('E-mail address')),
                                           (3, _('IP Address'))
                                          ))