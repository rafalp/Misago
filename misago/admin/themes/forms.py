from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from ...themes.models import Theme
from ..forms import YesNoSwitch
from .assets import create_css, create_image


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


class UploadAssetsForm(forms.Form):
    assets = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    def __init__(self, *args, instance=None):
        self.instance = instance
        super().__init__(*args)

    def clean(self):
        cleaned_data = super(UploadAssetsForm, self).clean()
        return cleaned_data

    def get_uploaded_assets(self):
        return self.files.getlist('assets')


class UploadCssForm(UploadAssetsForm):
    def save(self):
        for css in self.get_uploaded_assets():
            create_css(self.instance, css)
        return True


class UploadImagesForm(UploadAssetsForm):
    assets = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    def save(self):
        for image in self.get_uploaded_assets():
            create_image(self.instance, image)
        return True
