from django.utils.html import conditional_escape, mark_safe
from django.utils.translation import ugettext_lazy as _
from floppyforms import fields, widgets
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField
from misago.forms.widgets import ReCaptchaWidget

class ForumChoiceField(TreeNodeChoiceField):
    """
    Custom forum choice field
    """
    widget = widgets.Select

    def __init__(self, *args, **kwargs):
        kwargs['level_indicator'] = u'- - '
        super(ForumChoiceField, self).__init__(*args, **kwargs)

    def _get_level_indicator(self, obj):
        level = getattr(obj, obj._mptt_meta.level_attr)
        return mark_safe(conditional_escape(self.level_indicator) * (level - 1))


class ForumMultipleChoiceField(TreeNodeMultipleChoiceField):
    widget = widgets.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        kwargs['level_indicator'] = u'- - '
        super(ForumMultipleChoiceField, self).__init__(*args, **kwargs)

    def _get_level_indicator(self, obj):
        level = getattr(obj, obj._mptt_meta.level_attr)
        return mark_safe(conditional_escape(self.level_indicator) * (level - 1))


class ReCaptchaField(fields.CharField):
    widget = ReCaptchaWidget
    api_error = None

    def __init__(self, *args, **kwargs):
        kwargs['label'] = _("Verification Code")
        kwargs['help_text'] = _("Enter the code from image into the text field.")
        kwargs['required'] = False
        super(ReCaptchaField, self).__init__(*args, **kwargs)


class QACaptchaField(fields.CharField):
    pass
