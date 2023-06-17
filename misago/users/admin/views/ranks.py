from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.views import generic
from ...models import Rank
from ..forms import RankForm


class RankAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:ranks:index"
    model = Rank
    form_class = RankForm
    templates_dir = "misago/admin/ranks"
    message_404 = pgettext_lazy("admin ranks", "Requested rank does not exist.")

    def update_roles(self, target, roles):
        target.roles.clear()
        if roles:
            target.roles.add(*roles)

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        self.update_roles(target, form.cleaned_data["roles"])


class RanksList(RankAdmin, generic.ListView):
    ordering = (("order", None),)


class NewRank(RankAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy("admin ranks", 'New rank "%(name)s" has been saved.')


class EditRank(RankAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy("admin ranks", 'Rank "%(name)s" has been edited.')


class DeleteRank(RankAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        message_format = {"name": target.name}
        if target.is_default:
            message = pgettext(
                "admin ranks", 'Rank "%(name)s" is default rank and can\'t be deleted.'
            )
            return message % message_format
        if target.user_set.exists():
            message = pgettext(
                "admin ranks",
                'Rank "%(name)s" is assigned to users and can\'t be deleted.',
            )
            return message % message_format

    def button_action(self, request, target):
        target.delete()
        message = pgettext("admin ranks", 'Rank "%(name)s" has been deleted.')
        messages.success(request, message % {"name": target.name})


class MoveDownRank(RankAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = Rank.objects.filter(order__gt=target.order)
            other_target = other_target.earliest("order")
        except Rank.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])

            message = pgettext(
                "admin ranks", 'Rank "%(name)s" has been moved below "%(other)s".'
            )
            targets_names = {"name": target.name, "other": other_target.name}
            messages.success(request, message % targets_names)


class MoveUpRank(RankAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = Rank.objects.filter(order__lt=target.order)
            other_target = other_target.latest("order")
        except Rank.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])

            message = pgettext(
                "admin ranks", 'Rank "%(name)s" has been moved above "%(other)s".'
            )
            targets_names = {"name": target.name, "other": other_target.name}
            messages.success(request, message % targets_names)


class RankUsers(RankAdmin, generic.TargetedView):
    def real_dispatch(self, request, target):
        redirect_url = reverse("misago:admin:users:index")
        return redirect("%s?rank=%s" % (redirect_url, target.pk))


class DefaultRank(RankAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_default:
            message = pgettext("admin ranks", 'Rank "%(name)s" is already default.')
            return message % {"name": target.name}

    def button_action(self, request, target):
        Rank.objects.make_rank_default(target)
        message = pgettext("admin ranks", 'Rank "%(name)s" has been made default.')
        messages.success(request, message % {"name": target.name})
