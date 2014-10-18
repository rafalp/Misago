from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.threads import moderation
from misago.threads.views.generic.actions import ActionsBase


__all__ = ['Actions']


class Actions(ActionsBase):
    select_items_message = ugettext_lazy(
        "You have to select at least one thread.")
    is_mass_action = True

    def action_approve(self, request, threads):
        changed_threads = 0
        for thread in threads:
            if moderation.approve_thread(request.user, thread):
                changed_threads += 1

        if changed_threads:
            message = ungettext(
                '%(changed)d thread was approved.',
                '%(changed)d threads were approved.',
            changed_threads)
            messages.success(request, message % {'changed': changed_threads})
        else:
            message = _("No threads were approved.")
            messages.info(request, message)
