from django import forms
from django.utils.translation import gettext as _

from ..models import AttachmentType


def get_searchable_filetypes():
    choices = [(0, _("All types"))]
    choices += [(a.id, a.name) for a in AttachmentType.objects.order_by("name")]
    return choices


class FilterAttachmentsForm(forms.Form):
    uploader = forms.CharField(label=_("Uploader name contains"), required=False)
    filename = forms.CharField(label=_("Filename contains"), required=False)
    filetype = forms.TypedChoiceField(
        label=_("File type"),
        coerce=int,
        choices=get_searchable_filetypes,
        empty_value=0,
        required=False,
    )
    is_orphan = forms.ChoiceField(
        label=_("State"),
        required=False,
        choices=[
            ("", _("All")),
            ("yes", _("Only orphaned")),
            ("no", _("Not orphaned")),
        ],
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("uploader"):
            queryset = queryset.filter(
                uploader_slug__contains=criteria["uploader"].lower()
            )
        if criteria.get("filename"):
            queryset = queryset.filter(filename__icontains=criteria["filename"])
        if criteria.get("filetype"):
            queryset = queryset.filter(filetype_id=criteria["filetype"])
        if criteria.get("is_orphan") == "yes":
            queryset = queryset.filter(post__isnull=True)
        elif criteria.get("is_orphan") == "no":
            queryset = queryset.filter(post__isnull=False)
        return queryset


class AttachmentTypeForm(forms.ModelForm):
    class Meta:
        model = AttachmentType
        fields = "__all__"
        labels = {
            "name": _("Type name"),
            "extensions": _("File extensions"),
            "mimetypes": _("Mimetypes"),
            "size_limit": _("Maximum allowed uploaded file size"),
            "status": _("Status"),
            "limit_uploads_to": _("Limit uploads to"),
            "limit_downloads_to": _("Limit downloads to"),
        }
        help_texts = {
            "extensions": _(
                "List of comma separated file extensions associated with this "
                "attachment type."
            ),
            "mimetypes": _(
                "Optional list of comma separated mime types associated with this "
                "attachment type."
            ),
            "size_limit": _(
                "Maximum allowed uploaded file size for this type, in kb. "
                "May be overriden via user permission."
            ),
            "status": _("Controls this attachment type availability on your site."),
            "limit_uploads_to": _(
                "If you wish to limit option to upload files of this type to users "
                "with specific roles, select them on this list. Otherwhise don't "
                "select any roles to allow all users with permission to upload "
                "attachments to be able to upload attachments of this type."
            ),
            "limit_downloads_to": _(
                "If you wish to limit option to download files of this type to users "
                "with specific roles, select them on this list. Otherwhise don't "
                "select any roles to allow all users with permission to download "
                "attachments to be able to download attachments of this type."
            ),
        }
        widgets = {
            "limit_uploads_to": forms.CheckboxSelectMultiple,
            "limit_downloads_to": forms.CheckboxSelectMultiple,
        }

    def clean_extensions(self):
        data = self.clean_list(self.cleaned_data["extensions"])
        if not data:
            raise forms.ValidationError(_("This field is required."))
        return data

    def clean_mimetypes(self):
        data = self.cleaned_data["mimetypes"]
        if data:
            return self.clean_list(data)

    def clean_list(self, value):
        items = [v.lstrip(".") for v in value.lower().replace(" ", "").split(",")]
        return ",".join(set(filter(bool, items)))
