from django import forms
from django.utils.translation import pgettext_lazy

from ...attachments.models import AttachmentType


def get_searchable_filetypes():
    choices = [(0, pgettext_lazy("admin attachments type filter choice", "All types"))]
    choices += [(a.id, a.name) for a in AttachmentType.objects.order_by("name")]
    return choices


class FilterAttachmentsForm(forms.Form):
    uploader = forms.CharField(
        label=pgettext_lazy("admin attachments filter form", "Uploader name contains"),
        required=False,
    )
    filename = forms.CharField(
        label=pgettext_lazy("admin attachments filter form", "Filename contains"),
        required=False,
    )
    filetype = forms.TypedChoiceField(
        label=pgettext_lazy("admin attachments filter form", "File type"),
        coerce=int,
        choices=get_searchable_filetypes,
        empty_value=0,
        required=False,
    )
    is_orphan = forms.ChoiceField(
        label=pgettext_lazy("admin attachments filter form", "State"),
        required=False,
        choices=[
            (
                "",
                pgettext_lazy(
                    "admin attachments orphan filter choice",
                    "All",
                ),
            ),
            (
                "yes",
                pgettext_lazy(
                    "admin attachments orphan filter choice",
                    "Only orphaned",
                ),
            ),
            (
                "no",
                pgettext_lazy(
                    "admin attachments orphan filter choice",
                    "Not orphaned",
                ),
            ),
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
