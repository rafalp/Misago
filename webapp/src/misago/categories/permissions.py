from django import forms
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from ..acl import algebra
from ..acl.decorators import return_boolean
from ..admin.forms import YesNoSwitch
from .models import Category, CategoryRole, RoleCategoryACL


class PermissionsForm(forms.Form):
    legend = _("Category access")

    can_see = YesNoSwitch(label=_("Can see category"))
    can_browse = YesNoSwitch(label=_("Can see category contents"))


def change_permissions_form(role):
    if isinstance(role, CategoryRole):
        return PermissionsForm


def build_acl(acl, roles, key_name):
    new_acl = {"visible_categories": [], "browseable_categories": [], "categories": {}}
    new_acl.update(acl)

    roles = get_categories_roles(roles)

    for category in Category.objects.all_categories():
        build_category_acl(new_acl, category, roles, key_name)

    return new_acl


def get_categories_roles(roles):
    queryset = RoleCategoryACL.objects.filter(role__in=roles)
    queryset = queryset.select_related("category_role")

    roles = {}
    for acl_relation in queryset.iterator():
        role = acl_relation.category_role
        roles.setdefault(acl_relation.category_id, []).append(role)
    return roles


def build_category_acl(acl, category, categories_roles, key_name):
    if category.level > 1:
        if category.parent_id not in acl["visible_categories"]:
            # dont bother with child categories of invisible parents
            return
        if not acl["categories"][category.parent_id]["can_browse"]:
            # parent's visible, but its contents aint
            return

    category_roles = categories_roles.get(category.pk, [])

    final_acl = {"can_see": 0, "can_browse": 0}

    algebra.sum_acls(
        final_acl,
        roles=category_roles,
        key=key_name,
        can_see=algebra.greater,
        can_browse=algebra.greater,
    )

    if final_acl["can_see"]:
        acl["visible_categories"].append(category.pk)
        acl["categories"][category.pk] = final_acl

        if final_acl["can_browse"]:
            acl["browseable_categories"].append(category.pk)


def add_acl_to_category(user_acl, target):
    target.acl["can_see"] = can_see_category(user_acl, target)
    target.acl["can_browse"] = can_browse_category(user_acl, target)


def serialize_categories_acls(user_acl):
    categories_acl = []
    for category, acl in user_acl.pop("categories").items():
        if acl["can_browse"]:
            categories_acl.append(
                {
                    "id": category,
                    "can_start_threads": acl.get("can_start_threads", False),
                    "can_reply_threads": acl.get("can_reply_threads", False),
                    "can_pin_threads": acl.get("can_pin_threads", 0),
                    "can_hide_threads": acl.get("can_hide_threads", 0),
                    "can_close_threads": acl.get("can_close_threads", False),
                }
            )
    user_acl["categories"] = categories_acl


def register_with(registry):
    registry.acl_annotator(Category, add_acl_to_category)
    registry.user_acl_serializer(serialize_categories_acls)


def allow_see_category(user_acl, target):
    try:
        category_id = target.pk
    except AttributeError:
        category_id = int(target)

    if not category_id in user_acl["visible_categories"]:
        raise Http404()


can_see_category = return_boolean(allow_see_category)


def allow_browse_category(user_acl, target):
    target_acl = user_acl["categories"].get(target.id, {"can_browse": False})
    if not target_acl["can_browse"]:
        message = _('You don\'t have permission to browse "%(category)s" contents.')
        raise PermissionDenied(message % {"category": target.name})


can_browse_category = return_boolean(allow_browse_category)
