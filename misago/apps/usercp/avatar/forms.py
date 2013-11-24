from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.conf import settings
from misago.forms import Form

class UploadAvatarForm(Form):
    avatar_upload = forms.ImageField(label= _("Upload Image File"),
                                     help_text= _("Select image file on your computer you wish to use as forum avatar. You will be able to crop image after upload. Animations will be stripped."),
                                     error_messages={'invalid_image': _("Uploaded file is not correct image.")})
    error_source = 'avatar_upload'

    def clean_avatar_upload(self):
        image = self.cleaned_data.get('avatar_upload', False)
        if image:
            if image._size > settings.upload_limit * 1024:
                if settings.upload_limit > 1024:
                    limit = '%s Mb' % "{:10.2f}".format(float(settings.upload_limit / 1024.0))
                else:
                    limit = '%s Kb' % settings.upload_limit
                raise ValidationError(_("Avatar image cannot be larger than %(limit)s.") % {'limit': limit})
        else:
            raise ValidationError(_("Couldn't read uploaded image"))
        return image
