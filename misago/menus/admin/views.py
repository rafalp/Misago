from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...admin.views import generic
from ..models import MenuLink
from .forms import MenuLinkForm
from .ordering import get_next_free_order


class MenuLinkAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:settings:links:index"
    model = MenuLink
    form_class = MenuLinkForm
    templates_dir = "misago/admin/menulinks"
    message_404 = _("Requested MenuLink does not exist.")

    def handle_form(self, form, request, target):
        form.save()

        if self.message_submit:
            messages.success(request, self.message_submit % {"title": target.title})


class MenuLinksList(MenuLinkAdmin, generic.ListView):
    ordering = (("order", None),)
    selection_label = _("With MenuLinks: 0")
    empty_selection_label = _("Select MenuLinks")
    mass_actions = [
        {
            "action": "delete",
            "name": _("Delete MenuLinks"),
            "confirmation": _("Are you sure you want to delete those MenuLinks?"),
        }
    ]

    def action_delete(self, request, items):
        items.delete()
        MenuLink.objects.invalidate_cache()
        messages.success(request, _("Selected MenuLinks have been deleted."))


class NewMenuLink(MenuLinkAdmin, generic.ModelFormView):
    message_submit = _('New MenuLink "%(title)s" has been saved.')

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        form.instance.order = get_next_free_order()
        form.instance.save()
        MenuLink.objects.invalidate_cache()


class EditMenuLink(MenuLinkAdmin, generic.ModelFormView):
    message_submit = _('MenuLink "%(title)s" has been edited.')

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        form.instance.save()
        MenuLink.objects.invalidate_cache()


class DeleteMenuLink(MenuLinkAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        MenuLink.objects.invalidate_cache()
        message = _('MenuLink "%(title)s" has been deleted.')
        messages.success(request, message % {"title": target.title})


class MoveDownMenuLink(MenuLinkAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = MenuLink.objects.filter(order__gt=target.order)
            other_target = other_target.earliest("order")
        except MenuLink.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])
            MenuLink.objects.invalidate_cache()

            message = _("Menu link to %(link)s has been moved after %(other)s.")
            targets_names = {"link": target, "other": other_target}
            messages.success(request, message % targets_names)


class MoveUpMenuLink(MenuLinkAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = MenuLink.objects.filter(order__lt=target.order)
            other_target = other_target.latest("order")
        except MenuLink.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])
            MenuLink.objects.invalidate_cache()

            message = _("Menu link to %(link)s has been moved before %(other)s.")
            targets_names = {"link": target, "other": other_target}
            messages.success(request, message % targets_names)
