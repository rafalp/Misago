from django import forms
from django.utils.translation import ugettext as _

from .models import AttachmentType


class AttachmentTypeForm(forms.ModelForm):
    class Meta:
        model = AttachmentType
        fields = '__all__'
        labels = {
            'name': _("Type name"),
            'extensions': _("File extensions"),
            'mimetypes': _("Mimetypes"),
            'size_limit': _("Maximum allowed uploaded file size"),
            'status': _("Status"),
            'limit_uploaders_to': _("Limit uploads to"),
            'limit_downloaders_to': _("Limit downloaders to"),
        }
        help_texts = {
            'extensions': _("List of comma separated file extensions associated with this attachment type."),
            'mimetypes': _("Optional list of comma separated mime types associated with this attachment type."),
            'size_limit': _("Maximum allowed uploaded file size for this type, in kb. "
                            "May be overriden via user permission."),
            'status': _("Controls this attachment type availability on your site."),
            'limit_uploaders_to': _("If you wish to limit option to upload files of this type to users with specific "
                                    "roles, select them on this list. Otherwhise don't select any roles to allow all "
                                    "users with permission to upload attachments to be able to upload attachments of "
                                    "this type."),
            'limit_downloaders_to': _("If you wish to limit option to download files of this type to users with "
                                      "specific roles, select them on this list. Otherwhise don't select any roles to "
                                      "allow all users with permission to download attachments to be able to download "
                                      " attachments of this type."),
        }
        widgets = {
            'limit_uploaders_to': forms.CheckboxSelectMultiple,
            'limit_downloaders_to': forms.CheckboxSelectMultiple,
        }

    def clean_extensions(self):
        data =  self.clean_list(self.cleaned_data['extensions'])
        if not data:
            raise forms.ValidationError(_("This field is required."))
        return data

    def clean_mimetypes(self):
        return self.clean_list(self.cleaned_data['mimetypes'])

    def clean_list(self, value):
        items = [v.lstrip('.') for v in value.lower().replace(' ', '').split(',')]
        return ','.join(set(filter(bool, items)))
