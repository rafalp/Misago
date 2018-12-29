from django import forms
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import gettext, gettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from ...themes.models import Theme
from ..forms import YesNoSwitch
from .css import create_css
from .media import create_media


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
    allowed_content_types = []
    allowed_extensions = []

    assets = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        error_messages={"required": _("No files have been uploaded.")},
    )

    def __init__(self, *args, instance=None):
        self.instance = instance
        super().__init__(*args)

    def clean_assets(self):
        assets = []
        for asset in self.files.getlist("assets"):
            try:
                if self.allowed_content_types:
                    self.validate_asset_content_type(asset)
                if self.allowed_extensions:
                    self.validate_asset_extension(asset)
            except forms.ValidationError as e:
                self.add_error("assets", e)
            else:
                assets.append(asset)

        return assets

    def validate_asset_content_type(self, asset):
        if asset.content_type in self.allowed_content_types:
            return

        message = gettext(
            'File "%(file)s" content type "%(content_type)s" is not allowed.'
        )
        details = {"file": asset.name, "content_type": asset.content_type}

        raise forms.ValidationError(message % details)

    def validate_asset_extension(self, asset):
        filename = asset.name.lower()
        for extension in self.allowed_extensions:
            if filename.endswith(".%s" % extension):
                return

        message = gettext('File "%(file)s" extension is invalid.')
        details = {"file": asset.name}

        raise forms.ValidationError(message % details)

    def save(self):
        for asset in self.cleaned_data["assets"]:
            self.save_asset(asset)


class UploadCssForm(UploadAssetsForm):
    allowed_content_types = ["text/css"]
    allowed_extensions = ["css"]

    def save_asset(self, asset):
        create_css(self.instance, asset)


class UploadMediaForm(UploadAssetsForm):
    def save_asset(self, asset):
        create_media(self.instance, asset)
