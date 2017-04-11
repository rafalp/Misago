from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.threads.models import Thread
from misago.threads.permissions import can_start_thread
from misago.threads.validators import validate_category, validate_title


__all__ = [
    'NewThreadSerializer',
]


class NewThreadSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.IntegerField()
    weight = serializers.IntegerField(
        required=False,
        allow_null=True,
        max_value=Thread.WEIGHT_GLOBAL,
        min_value=Thread.WEIGHT_DEFAULT,
    )
    is_hidden = serializers.NullBooleanField(required=False)
    is_closed = serializers.NullBooleanField(required=False)

    def validate_title(self, title):
        return validate_title(title)

    def validate_category(self, category_id):
        self.category = validate_category(self.context, category_id)
        if not can_start_thread(self.context, self.category):
            raise ValidationError(_("You can't create new threads in selected category."))
        return self.category

    def validate_weight(self, weight):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return weight  # don't validate weight further if category failed

        if weight > self.category.acl.get('can_pin_threads', 0):
            if weight == 2:
                raise ValidationError(
                    _("You don't have permission to pin threads globally in this category.")
                )
            else:
                raise ValidationError(
                    _("You don't have permission to pin threads in this category.")
                )
        return weight

    def validate_is_hidden(self, is_hidden):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return is_hidden  # don't validate hidden further if category failed

        if is_hidden and not self.category.acl.get('can_hide_threads'):
            raise ValidationError(_("You don't have permission to hide threads in this category."))
        return is_hidden

    def validate_is_closed(self, is_closed):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return is_closed  # don't validate closed further if category failed

        if is_closed and not self.category.acl.get('can_close_threads'):
            raise ValidationError(
                _("You don't have permission to close threads in this category.")
            )
        return is_closed
