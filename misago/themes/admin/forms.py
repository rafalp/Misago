import re

from django import forms
from django.core.files.base import ContentFile
from django.utils.translation import gettext, gettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from ...core.utils import get_file_hash
from ..models import Theme, Css
from .css import css_needs_rebuilding, create_css, get_next_css_order
from .media import create_media
from .validators import validate_css_name, validate_css_name_is_available


class ThemeChoiceField(TreeNodeChoiceField):
    level_indicator = "- - "

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("queryset", Theme.objects.all())
        kwargs.setdefault("empty_label", _("No parent"))
        kwargs.setdefault("level_indicator", self.level_indicator)
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


class ImportForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        help_text=_("Leave this field empty to use theme name from imported file."),
        max_length=255,
        required=False,
    )
    parent = ThemeChoiceField(label=_("Parent"), required=False)
    upload = forms.FileField(
        label=_("Theme file"), help_text=_("Theme file should be a ZIP file.")
    )

    def clean_upload(self):
        data = self.cleaned_data["upload"]
        error_message = gettext("Uploaded file is not a valid ZIP file.")
        if not data.name.lower().endswith(".zip"):
            raise forms.ValidationError(error_message)
        if data.content_type not in ("application/zip", "application/octet-stream"):
            raise forms.ValidationError(error_message)
        return data


class ThemeManifest(forms.Form):
    name = forms.CharField(max_length=255)
    version = forms.CharField(max_length=255, required=False)
    author = forms.CharField(max_length=255, required=False)
    url = forms.URLField(max_length=255, required=False)


class ThemeCssUrlManifest(forms.Form):
    name = forms.CharField(max_length=255)
    url = forms.URLField(max_length=255)


def create_css_file_manifest(allowed_path):
    class ThemeCssFileManifest(forms.Form):
        name = forms.CharField(max_length=255, validators=[validate_css_name])
        path = forms.FilePathField(
            allowed_path, match=re.compile(r"\.css$", re.IGNORECASE)
        )

    return ThemeCssFileManifest


def create_media_file_manifest(allowed_path):
    class ThemeMediaFileManifest(forms.Form):
        name = forms.CharField(max_length=255)
        type = forms.CharField(max_length=255)
        path = forms.FilePathField(allowed_path)

    return ThemeMediaFileManifest


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


class CssEditorForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        help_text=_(
            "Should be an correct filename and include the .css extension. It will be lowercased."
        ),
        validators=[validate_css_name],
    )
    source = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Css
        fields = ["name"]

    def clean_name(self):
        data = self.cleaned_data["name"]
        validate_css_name_is_available(self.instance, data)
        return data

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("source"):
            raise forms.ValidationError(gettext("You need to enter CSS for this file."))
        return cleaned_data

    def save(self):
        name = self.cleaned_data["name"]
        source = self.cleaned_data["source"].encode("utf-8")
        source_file = ContentFile(source, name)

        self.instance.name = name

        if self.instance.source_file:
            self.instance.source_file.delete(save=False)

        self.instance.source_file = source_file
        self.instance.source_hash = get_file_hash(source_file)
        self.instance.source_needs_building = css_needs_rebuilding(source_file)
        self.instance.size = len(source)

        if not self.instance.pk:
            self.instance.order = get_next_css_order(self.instance.theme)

        self.instance.save()
        return self.instance


class CssLinkForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Link name"),
        help_text=_('Can be descriptive (e.g. "roboto from fonts.google.com").'),
    )
    url = forms.URLField(label=_("Remote CSS URL"))

    class Meta:
        model = Css
        fields = ["name", "url"]

    def clean_name(self):
        data = self.cleaned_data["name"]
        validate_css_name_is_available(self.instance, data)
        return data

    def save(self):
        if not self.instance.pk:
            self.instance.order = get_next_css_order(self.instance.theme)
            self.instance.save()
        else:
            self.instance.save(update_fields=["name", "url", "modified_on"])

        return self.instance
