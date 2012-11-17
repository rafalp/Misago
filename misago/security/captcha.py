from django.forms.fields import CharField
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from recaptcha.client.captcha import API_SSL_SERVER, API_SERVER, VERIFY_SERVER

class ReCaptchaWidget(TextInput):
    pass


class ReCaptchaField(CharField):
    widget = ReCaptchaWidget # Fakey widget for FormLayout
    api_error = None # Api error
    def __init__(self, label=_("Verification Code"), *args, **kwargs):
        kwargs['label'], kwargs['required'] = label, False
        super(ReCaptchaField, self).__init__(*args, **kwargs)


class QACaptchaField(CharField):
    pass


def get_captcha_dict(settings, api_error = None):
    error_param = ''
    if api_error:
        error_param = '&error=%s' % api_error
    return {
            'api_server': API_SERVER,
            'public_key': settings['recaptcha_public'],
            'error_param': error_param,
            }