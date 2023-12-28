from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.views import generic
from ....cache.enums import CacheName
from ....cache.versions import invalidate_cache
from ...groups import count_groups_members, delete_group
from ...models import Group


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
        return context


class OrderingView(GroupAdmin, generic.OrderingView):
    def order_items(self, request, items: list[Group]):
        items_update = []
        for ordering, item in enumerate(items):
            item.ordering = ordering
            items_update.append(item)

        Group.objects.bulk_update(items_update, ["ordering"])


class MembersView(GroupAdmin, generic.TargetedView):
    def real_dispatch(self, request, target):
        redirect_url = reverse("misago:admin:users:index")
        return redirect(f"{redirect_url}?group={target.pk}")


class MembersMainView(GroupAdmin, generic.TargetedView):
    def real_dispatch(self, request, target):
        redirect_url = reverse("misago:admin:users:index")
        return redirect(f"{redirect_url}?main_group={target.pk}")


class NewView(GroupAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy(
        "admin groups", 'New group "%(name)s" has been saved.'
    )


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
        invalidate_cache(CacheName.PERMISSIONS)

        message = pgettext("admin groups", 'The "%(name)s" group has been deleted.')
        messages.success(request, message % {"name": target.name})


class MakeDefaultView(GroupAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_default:
            message = pgettext("admin groups", 'Group "%(name)s" is already default.')
            return message % {"name": target.name}

    def button_action(self, request, target):
        Group.objects.filter(id=target.id).update(is_default=True)
        Group.objects.exclude(id=target.id).update(is_default=False)

        message = pgettext("admin groups", 'Group "%(name)s" has been made default.')
        messages.success(request, message % {"name": target.name})
