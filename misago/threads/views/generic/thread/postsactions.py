from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.threads import moderation
from misago.threads.views.generic.actions import ActionsBase


__all__ = ['PostsActions']


class PostsActions(ActionsBase):
    select_items_message = ugettext_lazy(
        "You have to select at least one post.")
    is_mass_action = True

    def get_available_actions(self, kwargs):
        self.thread = kwargs['thread']
        self.forum = self.thread.forum

        actions = []

        if self.forum.acl['can_hide_posts']:
            actions.append({
                'action': 'unhide',
                'icon': 'eye',
                'name': _("Unhide posts")
            })
            actions.append({
                'action': 'hide',
                'icon': 'eye-slash',
                'name': _("Hide posts")
            })
        if self.forum.acl['can_hide_posts'] == 2:
            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete posts"),
                'confirmation': _("Are you sure you want to delete selected "
                                  "posts? This action can't be undone.")
            })

        return actions

    def action_unhide(self, request, posts):
        pass

    def action_hide(self, request, posts):
        pass

    def action_delete(self, request, posts):
        pass
