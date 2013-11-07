from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, ForumMultipleChoiceField
from misago.models import Role, Forum
from misago.validators import validate_sluggable

class PrefixForm(Form):
    name = forms.CharField(label=_("Prefix Name"),
                           max_length=16, validators=[validate_sluggable(
                                                                          _("Prefix must contain alphanumeric characters."),
                                                                          _("Prefix name is too long.")
                                                                          )])
    style = forms.CharField(label=_("Prefix CSS Class"),
                            help_text=_("CSS class that will be used to style this thread prefix."),
                            max_length=255, required=False)
    forums = ForumMultipleChoiceField(label=_("Prefix Forums"),
                                      help_text=_("Select forums in which this prefix will be available."),
                                      level_indicator=u'- - ',
                                      queryset=Forum.objects.get(special='root').get_descendants())
