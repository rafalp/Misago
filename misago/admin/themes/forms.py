from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from ...theming.models import Theme
from ..forms import YesNoSwitch


class ThemeChoiceField(TreeNodeChoiceField):
    level_indicator = "- - "

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("queryset", Theme.objects.all())
        kwargs.setdefault("empty_label", _("No parent"))
        super().__init__(*args, **kwargs)


class ThemeForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"))
    parent = ThemeChoiceField(label=_("Parent"), required=False)
    version = forms.CharField(label=_("Version"), required=False)
    author = forms.CharField(label=_("Author(s)"), required=False)
    url = forms.URLField(label=_("Url"), required=False)

    class Meta:
        model = Theme
        fields = ["name", "parent", "version", "author", "url"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit_parent_choices()

    def limit_parent_choices(self):
        if not self.instance or not self.instance.pk:
            return

        self.fields["parent"].queryset = Theme.objects.exclude(
            tree_id=self.instance.tree_id,
            lft__gte=self.instance.lft,
            rght__lte=self.instance.rght,
        )
