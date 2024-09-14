from django import forms
from django.utils.translation import pgettext, pgettext_lazy

from ...attachments.models import AttachmentType


class AttachmentTypeForm(forms.ModelForm):
    class Meta:
        model = AttachmentType
        fields = [
            "name",
            "extensions",
            "mimetypes",
            "size_limit",
            "status",
            "limit_uploads_to",
            "limit_downloads_to",
        ]
        labels = {
            "name": pgettext_lazy("admin attachment type form", "Type name"),
            "extensions": pgettext_lazy(
                "admin attachment type form", "File extensions"
            ),
            "mimetypes": pgettext_lazy("admin attachment type form", "Mimetypes"),
            "size_limit": pgettext_lazy(
                "admin attachment type form", "Maximum allowed uploaded file size"
            ),
            "status": pgettext_lazy("admin attachment type form", "Status"),
            "limit_uploads_to": pgettext_lazy(
                "admin attachment type form", "Limit uploads to"
            ),
            "limit_downloads_to": pgettext_lazy(
                "admin attachment type form", "Limit downloads to"
            ),
        }
        help_texts = {
            "extensions": pgettext_lazy(
                "admin attachment type form",
                "List of comma separated file extensions associated with this attachment type.",
            ),
            "mimetypes": pgettext_lazy(
                "admin attachment type form",
                "Optional list of comma separated mime types associated with this attachment type.",
            ),
            "size_limit": pgettext_lazy(
                "admin attachment type form",
                "Maximum allowed uploaded file size for this type, in kb. This setting is deprecated and has no effect. It will be deleted in Misago 1.0.",
            ),
            "status": pgettext_lazy(
                "admin attachment type form",
                "Controls this attachment type availability on your site.",
            ),
            "limit_uploads_to": pgettext_lazy(
                "admin attachment type form",
                "If you wish to limit option to upload files of this type to users with specific roles, select them on this list. Otherwise don't select any roles to allow all users with permission to upload attachments to be able to upload attachments of this type.",
            ),
            "limit_downloads_to": pgettext_lazy(
                "admin attachment type form",
                "If you wish to limit option to download files of this type to users with specific roles, select them on this list. Otherwise don't select any roles to allow all users with permission to download attachments to be able to download attachments of this type.",
            ),
        }
        widgets = {
            "limit_uploads_to": forms.CheckboxSelectMultiple,
            "limit_downloads_to": forms.CheckboxSelectMultiple,
        }

    def clean_extensions(self):
        data = self.clean_list(self.cleaned_data["extensions"])
        if not data:
            raise forms.ValidationError(
                pgettext("admin attachment type form", "This field is required.")
            )
        return data

    def clean_mimetypes(self):
        data = self.cleaned_data["mimetypes"]
        if data:
            return self.clean_list(data)

    def clean_list(self, value):
        items = [v.lstrip(".") for v in value.lower().replace(" ", "").split(",")]
        return ",".join(set(filter(bool, items)))
