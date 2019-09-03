from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...admin.views import generic
from ..models import MenuLink
from .forms import MenuLinkForm, FilterMenuLinksForm


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
    items_per_page = 30
    ordering = [("-id", _("From newest")), ("id", _("From oldest"))]
    filter_form = FilterMenuLinksForm
    selection_label = _("With MenuLinks: 0")
    empty_selection_label = _("Select MenuLinks")
    mass_actions = [
        {
            "action": "delete",
            "name": _("Delete MenuLinks"),
            "confirmation": _("Are you sure you want to delete those MenuLinks?"),
        }
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related()

    def action_delete(self, request, items):
        items.delete()
        MenuLink.objects.invalidate_cache()
        messages.success(request, _("Selected MenuLinks have been deleted."))


class NewMenuLink(MenuLinkAdmin, generic.ModelFormView):
    message_submit = _('New MenuLink "%(title)s" has been saved.')

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)

        form.instance.set_created_by(request.user)
        form.instance.save()
        MenuLink.objects.invalidate_cache()


class EditMenuLink(MenuLinkAdmin, generic.ModelFormView):
    message_submit = _('MenuLink "%(title)s" has been edited.')

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)

        form.instance.last_modified_on = timezone.now()
        form.instance.set_last_modified_by(request.user)
        form.instance.save()
        MenuLink.objects.invalidate_cache()


class DeleteMenuLink(MenuLinkAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        MenuLink.objects.invalidate_cache()
        message = _('MenuLink "%(title)s" has been deleted.')
        messages.success(request, message % {"title": target.title})
