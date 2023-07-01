from django.contrib import messages
from django.utils.translation import pgettext_lazy

from ...admin.views import generic
from ..models import MenuItem
from ..cache import clear_menus_cache
from .forms import MenuItemForm
from .ordering import get_next_free_order


class MenuItemAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:settings:menu-items:index"
    model = MenuItem
    form_class = MenuItemForm
    templates_dir = "misago/admin/menuitems"
    message_404 = pgettext_lazy(
        "admin menu items", "Requested menu item does not exist."
    )

    def handle_form(self, form, request, target):
        form.save()

        if self.message_submit:
            messages.success(request, self.message_submit % {"item": target})


class MenuItemsList(MenuItemAdmin, generic.ListView):
    ordering = (("order", None),)
    mass_actions = [
        {
            "action": "delete",
            "name": pgettext_lazy("admin menu items", "Delete items"),
            "confirmation": pgettext_lazy(
                "admin menu items", "Are you sure you want to delete those menu items?"
            ),
        }
    ]

    def action_delete(self, request, items):
        items.delete()
        clear_menus_cache()
        messages.success(
            request,
            pgettext_lazy("admin menu items", "Selected menu items have been deleted."),
        )


class NewMenuItem(MenuItemAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy(
        "admin menu items", "New menu item %(item)s has been saved."
    )

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        form.instance.order = get_next_free_order()
        form.instance.save()
        clear_menus_cache()


class EditMenuItem(MenuItemAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy(
        "admin menu items", "Menu item %(item)s has been edited."
    )

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        form.instance.save()
        clear_menus_cache()


class DeleteMenuItem(MenuItemAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        clear_menus_cache()
        message = pgettext_lazy(
            "admin menu items", "Menu item %(item)s has been deleted."
        )
        messages.success(request, message % {"item": target})


class MoveDownMenuItem(MenuItemAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = MenuItem.objects.filter(order__gt=target.order)
            other_target = other_target.earliest("order")
        except MenuItem.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])
            clear_menus_cache()

            message = pgettext_lazy(
                "admin menu items", "Menu item %(item)s has been moved after %(other)s."
            )
            targets_names = {"item": target, "other": other_target}
            messages.success(request, message % targets_names)


class MoveUpMenuItem(MenuItemAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = MenuItem.objects.filter(order__lt=target.order)
            other_target = other_target.latest("order")
        except MenuItem.DoesNotExist:
            other_target = None

        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=["order"])
            target.save(update_fields=["order"])
            clear_menus_cache()

            message = pgettext_lazy(
                "admin menu items",
                "Menu item %(item)s has been moved before %(other)s.",
            )
            targets_names = {"item": target, "other": other_target}
            messages.success(request, message % targets_names)
