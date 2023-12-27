from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.views import generic
from ...groups import count_groups_members
from ...models import Group


class GroupAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:users:index"
    templates_dir = "misago/admin/groups"
    model = Group


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
        if target.is_default:
            message = pgettext(
                "admin groups",
                'Group "%(name)s" is a default group and can\'t be deleted.',
            )
            return message % message_format
        if target.user_set.exists():
            message = pgettext(
                "admin groups",
                'Group "%(name)s" is assigned to users and can\'t be deleted.',
            )
            return message % message_format

    def button_action(self, request, target):
        target.delete()
        message = pgettext("admin groups", 'Group "%(name)s" has been deleted.')
        messages.success(request, message % {"name": target.name})


class MakeDefaultView(GroupAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_default:
            message = pgettext("admin ranks", 'Group "%(name)s" is already default.')
            return message % {"name": target.name}

    def button_action(self, request, target):
        Group.objects.make_rank_default(target)
        message = pgettext("admin ranks", 'Group "%(name)s" has been made default.')
        messages.success(request, message % {"name": target.name})
