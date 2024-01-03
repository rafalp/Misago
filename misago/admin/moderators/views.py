from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import pgettext, pgettext_lazy

from ...cache.enums import CacheName
from ...cache.versions import invalidate_cache
from ...permissions.models import Moderator
from ...users.models import Group
from ..views import generic
from .forms import ModeratorForm, NewModeratorModalForm

User = get_user_model()


class ModeratorAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:moderators:index"
    templates_dir = "misago/admin/moderators"
    model = Moderator
    message_404 = pgettext_lazy(
        "admin moderators", "Requested moderator does not exist."
    )


class ListView(ModeratorAdmin, generic.ListView):
    def get_queryset(self):
        return self.get_model().objects.prefetch_related("group", "user")

    def process_context(self, request, context):
        context["items"] = sort_moderators(context["items"])

        context["new_moderator_form"] = NewModeratorModalForm(
            auto_id="new_moderator_form_%s",
        )
        return context


def sort_moderators(items):
    groups = []
    users = []

    for item in items:
        if item.group_id:
            groups.append(item)
        else:
            users.append(item)

    groups = sorted(groups, key=lambda i: i.group.id)
    users = sorted(users, key=lambda i: i.user.username)
    return groups + users


class NewView(ModeratorAdmin, generic.ModelFormView):
    template_name = "form.html"
    form_class = ModeratorForm

    def get_target(self, request, kwargs):
        if kwargs.get("group"):
            group = Group.objects.get(id=kwargs["group"])
            return Moderator(group=group)
        else:
            user = User.objects.get(id=kwargs["user"])
            return Moderator(user=user)

    def real_dispatch(self, request, target):
        # If moderator already exists for given group or user, redirect to it
        if target.group_id:
            instance = Moderator.objects.filter(group=target.group).first()
        else:
            instance = Moderator.objects.filter(user=target.user).first()
        if instance:
            return redirect(
                reverse("misago:admin:moderators:edit", kwargs={"pk": instance.id})
            )

        return super().real_dispatch(request, target)

    def check_permissions(self, request, target):
        if target.group and target.group.is_default:
            return pgettext_lazy(
                "admin moderators",
                "Can't grant \"%(target)s\" moderator permissions because it's the default group.",
            )

        if target.group and target.group.is_protected:
            return pgettext_lazy(
                "admin moderators",
                "Can't grant \"%(target)s\" moderator permissions because it's protected group.",
            )

    def handle_form(self, data, request, target):
        super().handle_form(data, request, target)
        invalidate_cache(CacheName.MODERATORS)


class EditView(ModeratorAdmin, generic.ModelFormView):
    template_name = "form.html"
    form_class = ModeratorForm
    success_message = pgettext_lazy(
        "admin moderators", '"%(name)s" moderator has been updated.'
    )

    def check_permissions(self, request, target):
        if target.is_protected:
            return pgettext(
                "admin moderators",
                'Can\'t change "%(target)s" moderator permissions because they are protected.',
            ) % {"target": target.group}

    def handle_form(self, data, request, target):
        super().handle_form(data, request, target)
        invalidate_cache(CacheName.MODERATORS)


class DeleteView(ModeratorAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_protected:
            return pgettext(
                "admin moderators",
                'Can\'t remove "%(target)s" moderator permissions because they are protected.',
            ) % {"target": target.group}

    def button_action(self, request, target):
        target.delete()
        invalidate_cache(CacheName.MODERATORS)

        message = pgettext("admin moderators", '"%(name)s" moderator has been deleted.')
        messages.success(request, message % {"name": target.name})
