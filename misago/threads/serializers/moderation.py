from django.forms import ValidationError
from django.utils.translation import ugettext as _

from rest_framework import serializers

from misago.acl import add_acl
from misago.categories.models import CATEGORIES_TREE_ID, Category
from misago.categories.permissions import can_see_category, can_browse_category

from misago.threads.models import THREAD_WEIGHT_DEFAULT, THREAD_WEIGHT_GLOBAL
from misago.threads.permissions import allow_start_thread
from misago.threads.validators import validate_title


def validate_category(user, category_id, allow_root=False):
    try:
        category = Category.objects.get(
            tree_id=CATEGORIES_TREE_ID,
            id=category_id,
        )
    except Category.DoesNotExist:
        category = None

    # Skip ACL validation for root category?
    if allow_root and category and not category.level:
        return category

    if not category or not can_see_category(user, category):
        raise ValidationError(_("Requested category could not be found."))

    if not can_browse_category(user, category):
        raise ValidationError(
            _("You don't have permission to access this category."))
    return category


class MergeThreadsSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.IntegerField()
    top_category = serializers.IntegerField(required=False, allow_null=True)
    weight = serializers.IntegerField(
        required=False,
        allow_null=True,
        max_value=THREAD_WEIGHT_GLOBAL,
        min_value=THREAD_WEIGHT_DEFAULT,
    )
    is_closed = serializers.NullBooleanField(required=False)

    def validate_title(self, title):
        return validate_title(title)

    def validate_top_category(self, category_id):
        return validate_category(self.context, category_id, allow_root=True)

    def validate_category(self, category_id):
        self.category = validate_category(self.context, category_id)
        return self.category

    def validate_weight(self, weight):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return weight # don't validate weight further if category failed

        if weight > self.category.acl.get('can_pin_threads', 0):
            if weight == 2:
                raise ValidationError(_("You don't have permission to pin "
                                        "threads globally in this category."))
            else:
                raise ValidationError(_("You don't have permission to pin "
                                        "threads in this category."))
        return weight

    def validate_is_closed(self, is_closed):
        try:
            add_acl(self.context, self.category)
        except AttributeError:
            return is_closed # don't validate closed further if category failed

        if is_closed and not self.category.acl.get('can_close_threads'):
            raise ValidationError(_("You don't have permission to close "
                                    "threads in this category."))
        return is_closed