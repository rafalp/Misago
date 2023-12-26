from django.contrib import messages
from django.utils.translation import pgettext, pgettext_lazy

from ....admin.views import generic
from ...models import Ban
from ..forms.bans import BanForm, FilterBansForm


class BanAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:users:bans:index"
    model = Ban
    form_class = BanForm
    templates_dir = "misago/admin/bans"
    message_404 = pgettext_lazy("admin bans", "Requested ban does not exist.")

    def handle_form(self, form, request, target):
        super().handle_form(form, request, target)
        Ban.objects.invalidate_cache()


class BansList(BanAdmin, generic.ListView):
    items_per_page = 30
    ordering = [
        ("-id", pgettext_lazy("admin bans ordering choice", "From newest")),
        ("id", pgettext_lazy("admin bans ordering choice", "From oldest")),
        ("banned_value", pgettext_lazy("admin bans ordering choice", "A to z")),
        ("-banned_value", pgettext_lazy("admin bans ordering choice", "Z to a")),
    ]
    filter_form = FilterBansForm
    selection_label = pgettext_lazy("admin bans", "With bans: 0")
    empty_selection_label = pgettext_lazy("admin bans", "Select bans")
    mass_actions = [
        {
            "action": "delete",
            "name": pgettext_lazy("admin bans", "Remove bans"),
            "confirmation": pgettext_lazy(
                "admin bans", "Are you sure you want to remove those bans?"
            ),
        }
    ]

    def action_delete(self, request, items):
        items.delete()
        Ban.objects.invalidate_cache()
        messages.success(
            request, pgettext("admin bans", "Selected bans have been removed.")
        )


class NewBan(BanAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy("admin bans", 'New ban "%(name)s" has been saved.')


class EditBan(BanAdmin, generic.ModelFormView):
    message_submit = pgettext_lazy("admin bans", 'Ban "%(name)s" has been edited.')


class DeleteBan(BanAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        Ban.objects.invalidate_cache()
        message = pgettext("admin bans", 'Ban "%(name)s" has been removed.')
        messages.success(request, message % {"name": target.name})
