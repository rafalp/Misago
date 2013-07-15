from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form

class BanForm(Form):
    """
    New/Edit Ban form
    """
    test = forms.TypedChoiceField(choices=(
                                           (0, _('Ban Username and e-mail')),
                                           (1, _('Ban Username')),
                                           (2, _('Ban E-mail address')),
                                           (3, _('Ban IP Address'))
                                           ), coerce=int)
    reason_user = forms.CharField(widget=forms.Textarea, required=False)
    reason_admin = forms.CharField(widget=forms.Textarea, required=False)
    ban = forms.CharField(max_length=255)
    expires = forms.DateField(required=False)
    layout = (
               (
                 _("Ban Details"),
                 (
                  ('nested', (('test', {'label': _("Ban Rule"), 'help_text': _("Select ban type from list and define rule by entering it in text field. If you want to ban specific user, enter here either his Username or E-mail address. If you want to define blanket ban, you can use wildcard (\"*\"). For example to forbid all members from using name suggesting that member is an admin, you can set ban that forbids \"Admin*\" as username."), 'width': 25}),
                  ('ban', {'width': 75}))),
                  ('expires', {'label': _("Ban Expiration"), 'help_text': _("If you want to, you can set this ban's expiration date by entering it here using YYYY-MM-DD format. Otherwhise you can leave this field empty making this ban permanent.")}),
                 ),
                ),
                (
                 _("Ban Message"),
                 (
                  ('reason_user', {'label': _("User-visible Ban Message"), 'help_text': _("Optional Ban message that will be displayed to banned members.")}),
                  ('reason_admin', {'label': _("Team-visible Ban Message"), 'help_text': _("Optional Ban message that will be displayed to forum team members.")}),
                 ),
                ),
               )


class SearchBansForm(Form):
    ban = forms.CharField(required=False)
    reason = forms.CharField(required=False)
    test = forms.TypedMultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(
                                          (0, _('Username and e-mail')),
                                          (1, _('Username')),
                                          (2, _('E-mail address')),
                                          (3, _('IP Address'))
                                          ), coerce=int, required=False)
    layout = (
              (
               _("Search Bans"),
               (
                ('ban', {'label': _("Ban"), 'attrs': {'placeholder': _("Ban contains...")}}),
                ('reason', {'label': _("Messages"), 'attrs': {'placeholder': _("User or Team message contains...")}}),
                ('test', {'label': _("Type")}),
               ),
              ),
             )
