from django.utils.translation import pgettext_lazy

from ...permissions.models import Moderator
from ..views import generic
from .forms import NewModeratorModalForm


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
        context["new_moderator_form"] = NewModeratorModalForm(
            auto_id="new_moderator_form_%s",
        )
        return context


class NewView(ModeratorAdmin, generic.FormView):
    pass


class EditView(ModeratorAdmin, generic.FormView):
    pass


class DeleteView(ModeratorAdmin, generic.ButtonView):
    pass
