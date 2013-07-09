from mptt.forms import TreeNodeChoiceField
from recaptcha.client.captcha import API_SSL_SERVER, API_SERVER, VERIFY_SERVER
from floppyforms import fields
from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import ugettext_lazy as _
from misago.forms.widgets import ReCaptchaWidget

class ForumChoiceField(TreeNodeChoiceField):
    """
    Custom forum choice field
    """
    def __init__(self, *args, **kwargs):
        kwargs['level_indicator'] = u'- - '
        super(ForumChoiceField, self).__init__(*args, **kwargs)

    def _get_level_indicator(self, obj):
        level = getattr(obj, obj._mptt_meta.level_attr)
        return mark_safe(conditional_escape(self.level_indicator) * (level - 1))


class ReCaptchaField(fields.CharField):
    widget = ReCaptchaWidget
    api_error = None
    def __init__(self, label=_("Verification Code"), *args, **kwargs):
        kwargs['label'], kwargs['required'] = label, False
        super(ReCaptchaField, self).__init__(*args, **kwargs)


class QACaptchaField(fields.CharField):
    pass
