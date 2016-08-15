from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _, ugettext_lazy

from rest_framework import serializers

from misago.acl import add_acl
from misago.categories.models import THREADS_ROOT_NAME, Category
from misago.categories.permissions import can_see_category, can_browse_category

from . import PostingEndpoint, PostingMiddleware
from ...permissions.threads import allow_start_thread
from ...threadtypes import trees_map


class CategoryMiddleware(PostingMiddleware):
    """
    Middleware that validates category id and sets category on thread and post instances
    """
    def use_this_middleware(self):
        return self.mode == PostingEndpoint.START and self.tree_name == THREADS_ROOT_NAME

    def get_serializer(self):
        return CategorySerializer(self.user, data=self.request.data)

    def pre_save(self, serializer):
        category = serializer.category_cache

        add_acl(self.user, category)

        # set flags for savechanges middleware
        category.update_all = False
        category.update_fields = []

        # assign category to thread and post
        self.thread.category = category
        self.post.category = category


class CategorySerializer(serializers.Serializer):
    category = serializers.IntegerField(error_messages={
        'required': ugettext_lazy("You have to select category to post thread in."),
        'invalid': ugettext_lazy("Selected category is invalid.")
    })

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.category_cache = None

        super(CategorySerializer, self).__init__(*args, **kwargs)

    def validate_category(self, value):
        try:
            self.category_cache = Category.objects.get(
                pk=value,
                tree_id=trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
            )

            can_see = can_see_category(self.user, self.category_cache)
            can_browse = can_browse_category(self.user, self.category_cache)
            if not (self.category_cache.level and can_see and can_browse):
                raise PermissionDenied(_("Selected category is invalid."))

            allow_start_thread(self.user, self.category_cache)
        except PermissionDenied as e:
            raise serializers.ValidationError(e.args[0])
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                _("Selected category doesn't exist or you don't have permission to browse it."))
