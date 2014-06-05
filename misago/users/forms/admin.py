from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.core.validators import validate_sluggable
from misago.acl.models import Role
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
        label=_("Description"), max_length=2048, required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text=_("Optional description explaining function or status of "
                    "members distincted with this rank."))
    roles = forms.ModelMultipleChoiceField(
        label=_("User roles"), queryset=Role.objects.order_by('name'),
        required=False,  widget=forms.CheckboxSelectMultiple,
        help_text=_('Rank can give users with it additional roles.'))
    css_class = forms.CharField(
        label=_("CSS class"), required=False,
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
            'name',
            'description',
            'css_class',
            'title',
            'roles',
            'is_tab',
            'is_on_index',
        ]

    def clean(self):
        data = super(RankForm, self).clean()

        self.instance.set_name(data.get['name'])
        return data
