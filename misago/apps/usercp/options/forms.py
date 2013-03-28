from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form
from misago.utils.timezones import tzlist

class UserForumOptionsForm(Form):
    newsletters = forms.BooleanField(required=False)
    timezone = forms.ChoiceField(choices=tzlist())
    hide_activity = forms.TypedChoiceField(choices=(
                                                    (0, _("Show my presence to everyone")),
                                                    (1, _("Show my presence to people I follow")),
                                                    (2, _("Show my presence to nobody")),
                                                    ), coerce=int)
    subscribe_start = forms.TypedChoiceField(choices=(
                                                      (0, _("Don't watch")),
                                                      (1, _("Put on watched threads list")),
                                                      (2, _("Put on watched threads list and e-mail me when somebody replies")),
                                                      ), coerce=int)
    subscribe_reply = forms.TypedChoiceField(choices=(
                                                      (0, _("Don't watch")),
                                                      (1, _("Put on watched threads list")),
                                                      (2, _("Put on watched threads list and e-mail me when somebody replies")),
                                                      ), coerce=int)
    allow_pds = forms.TypedChoiceField(choices=(
                                                (0, _("From everyone")),
                                                (1, _("From everyone but not members I ignore")),
                                                (2, _("From members I follow")),
                                                (2, _("From nobody")),
                                                ), coerce=int)

    layout = (
              (
               _("Privacy"),
               (
                ('hide_activity', {'label': _("Your Visibility"), 'help_text': _("If you want to, you can limit other members ability to track your presence on forums.")}),
                ('allow_pds', {'label': _("Allow Private Threads Invitations"), 'help_text': _("If you wish, you can restrict who can invite you to private threads. Keep in mind some groups or members may be allowed to override this preference.")}),
                )
               ),
              (
               _("Forum Options"),
               (
                ('timezone', {'label': _("Your Current Timezone"), 'help_text': _("If dates and hours displayed by forums are inaccurate, you can fix it by adjusting timezone setting.")}),
                ('newsletters', {'label': _("Newsletters"), 'help_text': _("On occasion board administrator may want to send e-mail message to multiple members."), 'inline': _("Yes, I want to subscribe forum newsletter")}),
                )
               ),
              (
               _("Watching Threads"),
               (
                ('subscribe_start', {'label': _("Threads I start")}),
                ('subscribe_reply', {'label': _("Threads I reply to")}),
                )
               ),
              )
