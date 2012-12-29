from PIL import Image
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class UploadAvatarForm(Form):
    avatar_upload = forms.ImageField(error_messages={'invalid_image': _("Uploaded file is not correct image.")})
    error_source = 'avatar_upload'
    
    layout = [
              [
               None,
               [
                ('avatar_upload', {'label': _("Upload Image File"), 'help_text': _("Select image file on your computer you wish to use as forum avatar. You will be able to crop image after upload. Animations will be stripped.")}),
                ],
               ],
              ]
    
    def clean_avatar_upload(self):
        image = self.cleaned_data.get('avatar_upload',False)
        if image:
            if image._size > self.request.settings.upload_limit * 1024:
                if self.request.settings.upload_limit > 1024:
                    limit = '%s Mb' % "{:10.2f}".format(float(self.request.settings.upload_limit / 1024.0))
                else:
                    limit = '%s Kb' % self.request.settings.upload_limit
                raise ValidationError(_("Avatar image cannot be larger than %(limit)s.") % {'limit': limit})
        else:
            raise ValidationError(_("Couldn't read uploaded image"))
        return image