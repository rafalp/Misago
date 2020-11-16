from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from rest_framework import serializers

from . import PostingEndpoint, PostingMiddleware
from ....acl.objectacl import add_acl_to_obj
from ....categories import THREADS_ROOT_NAME
from ....categories.models import Category
from ....categories.permissions import can_browse_category, can_see_category
from ...permissions import allow_start_thread
from ...threadtypes import trees_map


class CategoryMiddleware(PostingMiddleware):
    """
    middleware that validates category id and sets category on thread and post instances
    """

    def use_this_middleware(self):
        if self.mode == PostingEndpoint.START:
            return self.tree_name == THREADS_ROOT_NAME
        return False

    def get_serializer(self):
        return CategorySerializer(self.user_acl, data=self.request.data)

    def pre_save(self, serializer):
        category = serializer.category_cache

        add_acl_to_obj(self.user_acl, category)

        # set flags for savechanges middleware
        category.update_all = False
        category.update_fields = []

        # assign category to thread and post
        self.thread.category = category
        self.post.category = category


class CategorySerializer(serializers.Serializer):
    category = serializers.IntegerField(
        error_messages={
            "required": gettext_lazy("You have to select category to post thread in."),
            "invalid": gettext_lazy("Selected category is invalid."),
        }
    )

    def __init__(self, user_acl, *args, **kwargs):
        self.user_acl = user_acl
        self.category_cache = None

        super().__init__(*args, **kwargs)

    def validate_category(self, value):
        try:
            self.category_cache = Category.objects.get(
                pk=value, tree_id=trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
            )

            can_see = can_see_category(self.user_acl, self.category_cache)
            can_browse = can_browse_category(self.user_acl, self.category_cache)
            if not (self.category_cache.level and can_see and can_browse):
                raise PermissionDenied(_("Selected category is invalid."))

            allow_start_thread(self.user_acl, self.category_cache)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                _(
                    "Selected category doesn't exist or "
                    "you don't have permission to browse it."
                )
            )
        except PermissionDenied as e:
            raise serializers.ValidationError(e.args[0])
