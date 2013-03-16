from django.utils.html import conditional_escape, mark_safe
from mptt.forms import TreeNodeChoiceField

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