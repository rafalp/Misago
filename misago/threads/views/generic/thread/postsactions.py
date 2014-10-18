from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.threads import moderation
from misago.threads.views.generic.actions import ActionsBase


__all__ = ['PostsActions']


class PostsActions(ActionsBase):
    select_items_message = ugettext_lazy(
        "You have to select at least one post.")
    is_mass_action = True

    def get_available_actions(self, kwargs):
        return []
