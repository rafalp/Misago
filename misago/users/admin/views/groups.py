from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.views import generic
from ....cache.enums import CacheName
from ....cache.versions import invalidate_cache
from ....permissions.copy import copy_group_permissions
from ...enums import DefaultGroupId
from ...groups import (
    count_groups_members,
    create_group,
    delete_group,
    set_default_group,
)
from ...models import Group
from ..forms.groups import NewGroupForm

INVALID_DEFAULT_GROUP_IDS = (
    DefaultGroupId.ADMINS,
    DefaultGroupId.MODERATORS,
    DefaultGroupId.GUESTS,
)


class GroupAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:groups:index"
    templates_dir = "misago/admin/groups"
    model = Group
    message_404 = pgettext_lazy("admin groups", "Requested group does not exist.")


class ListView(GroupAdmin, generic.ListView):
    def process_context(self, request, context):
        items = list(context["items"])
        items_dict = {item.id: item for item in items}

        for group_id, members_count in count_groups_members():
            items_dict[group_id].members_count = members_count

        context["items"] = items
        context["invalid_default_group_ids"] = INVALID_DEFAULT_GROUP_IDS
        return context


class OrderingView(GroupAdmin, generic.OrderingView):
    def order_items(self, request, items: list[Group]):
        items_update = []
        for ordering, item in enumerate(items):
            item.ordering = ordering
            items_update.append(item)

        Group.objects.bulk_update(items_update, ["ordering"])
        invalidate_cache(CacheName.GROUPS)


class MembersView(GroupAdmin, generic.TargetedView):
    def real_dispatch(self, request, target):
        redirect_url = reverse("misago:admin:users:index")
        return redirect(f"{redirect_url}?group={target.pk}")


class MembersMainView(GroupAdmin, generic.TargetedView):
    def real_dispatch(self, request, target):
        redirect_url = reverse("misago:admin:users:index")
        return redirect(f"{redirect_url}?main_group={target.pk}")


class NewView(GroupAdmin, generic.ModelFormView):
    template_name = "new.html"
    form_class = NewGroupForm
    message_submit = pgettext_lazy(
        "admin groups", 'The "%(name)s" group has been created.'
    )

    def handle_form(self, form, request, target):
        group = create_group(
            name=form.cleaned_data["name"],
            request=request,
            form=form,
        )

        if form.cleaned_data["copy_permissions"]:
            copy_group_permissions(
                form.cleaned_data["copy_permissions"], group, request
            )

        invalidate_cache(CacheName.GROUPS, CacheName.PERMISSIONS)

        messages.success(request, self.message_submit % {"name": group.name})
        return redirect("misago:admin:groups:edit", pk=group.pk)


class EditView(GroupAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy("admin groups", 'Group "%(name)s" has been edited.')


class DeleteView(GroupAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        message_format = {"name": target.name}

        if target.is_protected:
            return (
                pgettext(
                    "admin groups",
                    'Can\'t delete a protected group "%(name)s".',
                )
                % message_format
            )

        if target.is_default:
            return (
                pgettext(
                    "admin groups",
                    'Can\'t delete the default group "%(name)s".',
                )
                % message_format
            )

        if target.user_set.exists():
            return (
                pgettext(
                    "admin groups",
                    "Can't delete the \"%(name)s\" group because it's a main group for some users.",
                )
                % message_format
            )

    def button_action(self, request, target):
        delete_group(target, request)
        invalidate_cache(CacheName.GROUPS, CacheName.PERMISSIONS)

        message = pgettext("admin groups", 'The "%(name)s" group has been deleted.')
        messages.success(request, message % {"name": target.name})


class MakeDefaultView(GroupAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        message_format = {"name": target.name}

        if target.is_default:
            return (
                pgettext("admin groups", 'The "%(name)s" group is already the default.')
                % message_format
            )

        if target.id in INVALID_DEFAULT_GROUP_IDS:
            return (
                pgettext(
                    "admin groups", 'The "%(name)s" group can\'t be set as default.'
                )
                % message_format
            )

    def button_action(self, request, target):
        set_default_group(target, request)
        invalidate_cache(CacheName.GROUPS)

        message = pgettext(
            "admin groups", 'The "%(name)s" group has been made a default.'
        )
        messages.success(request, message % {"name": target.name})
