from django import forms
from django.utils.translation import pgettext_lazy

from ...attachments.filetypes import filetypes


def get_searchable_filetypes():
    choices = [("", pgettext_lazy("admin attachments type filter choice", "All types"))]
    choices.extend(filetypes.as_django_choices())
    return choices


class FilterAttachmentsForm(forms.Form):
    uploader = forms.CharField(
        label=pgettext_lazy("admin attachments filter form", "Uploader name contains"),
        required=False,
    )
    name = forms.CharField(
        label=pgettext_lazy("admin attachments filter form", "Name contains"),
        required=False,
    )
    filetype = forms.ChoiceField(
        label=pgettext_lazy("admin attachments filter form", "File type"),
        choices=get_searchable_filetypes,
        required=False,
    )
    status = forms.ChoiceField(
        label=pgettext_lazy("admin attachments filter form", "Status"),
        required=False,
        choices=[
            (
                "",
                pgettext_lazy(
                    "admin attachments status filter choice",
                    "All",
                ),
            ),
            (
                "posted",
                pgettext_lazy(
                    "admin attachments status filter choice",
                    "Posted",
                ),
            ),
            (
                "unused",
                pgettext_lazy(
                    "admin attachments status filter choice",
                    "Unused",
                ),
            ),
            (
                "deleted",
                pgettext_lazy(
                    "admin attachments status filter choice",
                    "Deleted",
                ),
            ),
            (
                "broken",
                pgettext_lazy(
                    "admin attachments status filter choice",
                    "Broken",
                ),
            ),
        ],
    )

    def filter_queryset(self, criteria, queryset):
        if criteria.get("uploader"):
            queryset = queryset.filter(
                uploader_slug__contains=criteria["uploader"].lower()
            )
        if criteria.get("name"):
            queryset = queryset.filter(name__icontains=criteria["name"])
        if criteria.get("filetype"):
            queryset = queryset.filter(filetype_id=criteria["filetype"])
        if criteria.get("status") == "posted":
            queryset = queryset.filter(post__isnull=False)
        elif criteria.get("status") == "unused":
            queryset = queryset.filter(post__isnull=True, is_deleted=False)
        elif criteria.get("status") == "deleted":
            queryset = queryset.filter(is_deleted=True)
        elif criteria.get("status") == "broken":
            queryset = queryset.filter(upload="")
        return queryset
