from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.users.models import Rank


class RankForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        validators=[validate_sluggable()],
        help_text=_('Short and descriptive name of all users with this rank. '
                    '"The Team" or "Game Masters" are good examples.'))
    title = forms.CharField(
        label=_("User title"), required=False,
        help_text=_('Optional, singular version of rank name displayed by '
                    'user names. For example "GM" or "Dev".'))
    description = forms.CharField(
        label=_("Description"), max_length=1024, required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Optional description explaining function or status of "
                    "members distincted with this rank."))
    style = forms.CharField(
        label=_("CSS Class"), required=False,
        help_text=_("Optional css class added to content belonging to this "
                    "rank owner."))
    is_tab = forms.BooleanField(
        label=_("Give rank dedicated tab on users list"), required=False,
        help_text=_("Selecting this option will make users with this rank "
                    "easily discoverable by others trough dedicated page on "
                    "forum users list."))
    is_on_index = forms.BooleanField(
        label=_("Show users online on forum index"), required=False,
        help_text=_("Selecting this option will make forum inform other "
                    "users of their availability by displaying them on forum "
                    "index page."))

    class Meta:
        model = Rank
        fields = [
            'name', 'description', 'style', 'title', 'is_tab', 'is_on_index'
        ]

    def clean_name(self):
        data = self.cleaned_data['name']
        self.instance.set_name(data)
        return data
