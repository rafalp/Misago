from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, YesNoSwitch
from misago.models import Role
from misago.validators import validate_sluggable

class RankForm(Form):
    name = forms.CharField(label=_("Rank Name"),
    					   help_text=_("Rank Name is used to identify rank in Admin Control Panel and is used as page and tab title if you decide to make this rank act as tab on users list."),
    					   max_length=255, validators=[validate_sluggable(
                                                                          _("Rank name must contain alphanumeric characters."),
                                                                          _("Rank name is too long.")
                                                                          )])
    description = forms.CharField(label=_("Rank Description"),
    							  help_text=_("If this rank acts as tab on users list, here you can enter optional description that will be displayed above list of users with this rank."),
    							  widget=forms.Textarea, required=False)
    title = forms.CharField(label=_("Rank Title"),
    						help_text=_("Short description of rank's bearer role in your community."),
    						max_length=255, required=False)
    style = forms.CharField(label=_("Rank CSS Class"),
    						help_text=_("Optional CSS class that will be added to different elements displaying rank's owner or his content, allowing you to make them stand out from other members."),
    						max_length=255, required=False)
    special = forms.BooleanField(label=_("Special Rank"),
    							 help_text=_("Special ranks are ignored during updates of user ranking, making them unattainable without admin ingerention."),
    							 widget=YesNoSwitch, required=False)
    as_tab = forms.BooleanField(label=_("As Tab on Users List"),
    							help_text=_("Should this rank have its own page on users list, containing rank's description and list of users that have it? This is good option for rank used by forum team members or members that should be visible and easily reachable."),
    							widget=YesNoSwitch, required=False)
    on_index = forms.BooleanField(label=_("Display members online"),
    							  help_text=_("Should users online with this rank be displayed on board index?"),
    							  widget=YesNoSwitch, required=False)
    criteria = forms.CharField(label=_("Rank Criteria"),
    						   help_text=_("This setting allows you to limit number of users that can attain this rank. Enter 0 to assign this rank to all members (good for default rank). To give this rank to 10% of most active members, enter \"10%\". To give this rank to 10 most active members, enter \"10\". This setting is ignored for special ranks as they don't participate in user's ranking updates."),
    						   max_length=255, initial='0', validators=[RegexValidator(regex='^(\d+)(%?)$', message=_('This is incorrect rank match rule.'))], required=False)
    roles = False

    def finalize_form(self):
        if self.request.user.is_god():
            self.add_field('roles', forms.ModelMultipleChoiceField(label=_("Rank Roles"),
            													   help_text=_("You can grant users with this rank extra roles to serve either as rewards or signs of trust to active members."),
            			   										   widget=forms.CheckboxSelectMultiple, queryset=Role.objects.order_by('name').all(), required=False))
        else:
            self.add_field('roles', forms.ModelMultipleChoiceField(label=_("Rank Roles"),
            													   help_text=_("You can grant users with this rank extra roles to serve either as rewards or signs of trust to active members."),
            			   										   widget=forms.CheckboxSelectMultiple, queryset=Role.objects.filter(protected__exact=False).order_by('name').all(), required=False))
