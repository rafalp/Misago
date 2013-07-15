from UserDict import IterableUserDict
from recaptcha.client.captcha import displayhtml
from django.utils import formats
from misago.conf import settings

class FormLayout(object):
    """
    Simple scaffold for dynamically generated forms that allows for better rendering.
    """
    def __init__(self, layout, form):
        raise NotImplementedError("Forms layouts are not yet implemented")