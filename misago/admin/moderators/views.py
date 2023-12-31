from django.utils.translation import pgettext_lazy

from ...permissions.models import CategoryModerator
from ..views import generic


class ModeratorAdmin(generic.AdminBaseMixin):
    root_link = "misago:admin:moderators:index"
    templates_dir = "misago/admin/moderators"
    model = CategoryModerator
    message_404 = pgettext_lazy(
        "admin moderators", "Requested moderator does not exist."
    )


class ListView(ModeratorAdmin, generic.ListView):
    pass
