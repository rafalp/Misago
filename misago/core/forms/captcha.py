from recaptcha.client.captcha import API_SSL_SERVER, API_SERVER, VERIFY_SERVER
from django.forms.fields import CharField
from django.forms.widgets import TextInput

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