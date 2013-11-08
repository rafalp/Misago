from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form
from misago.models import Role
from misago.validators import validate_sluggable

class AttachmentTypeForm(Form):
    name = forms.CharField(label=_("Type Name"),
                           max_length=256, validators=[validate_sluggable(
                                                                          _("Name must contain alphanumeric characters."),
                                                                          _("Type name is too long.")
                                                                          )])
    extensions = forms.CharField(label=_("File Extensions"),
                                 help_text=_("Enter file name extensions used by this attachment type. Don't enter dots. If this attachment type supports more than one extension, separate them with coma, for example: jpg,jpeg."),
                                 max_length=255)
    size_limit = forms.IntegerField(label=_("Hard File Size Limit"),
                                    help_text=_("In addition to role-based single uploaded file size limit you can set additional limit for all future attachments of this type. To set limit, enter number of kilobytes, otherwhise enter 0. If limit is defined, forum will use lower limit (this one or role one) during validation of uploaded file, unless uploader has no single uploaded file size limit, which is when uploaded file size validation is not performed."),
                                    min_value=0, initial=0)
    roles = forms.ModelMultipleChoiceField(label=_("Restrict to certain roles"), required=None,
                                           help_text=_("You can restrict uploading files of this type to users with certain roles by selecting them in above list."),
                                           queryset=Role.objects.order_by('name'), widget=forms.CheckboxSelectMultiple)

    def clean_extension(self, extension):
        extension = extension.strip().lower()
        try:
            while extension[0] == '.':
                extension = extension[1:]
        except IndexError:
            return None
        return extension

    def clean_extensions(self):
        clean_data = []
        data = self.cleaned_data['extensions'].strip().lower()
        for extension in data.split(','):
            extension = self.clean_extension(extension)
            if extension and not extension in clean_data:
                clean_data.append(extension)
        if not clean_data:
            raise forms.ValidationError(_("You have to specify at least one file extension."))
        return ','.join(clean_data)
