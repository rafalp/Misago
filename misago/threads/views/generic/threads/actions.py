from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.threads import moderation
from misago.threads.views.generic.actions import ActionsBase, ReloadAfterDelete


__all__ = ['Actions', 'ReloadAfterDelete']


class Actions(ActionsBase):
    select_items_message = ugettext_lazy(
        "You have to select at least one thread.")
    is_mass_action = True

    def redirect_after_deletion(self, request, queryset):
        paginator = Paginator(queryset, 20, 10)
        current_page = int(request.resolver_match.kwargs.get('page', 0))

        if paginator.num_pages < current_page:
            namespace = request.resolver_match.namespace
            url_name = request.resolver_match.url_name
            kwars = request.resolver_match.kwargs
            kwars['page'] = paginator.num_pages
            if kwars['page'] == 1:
                del kwars['page']
            return redirect('%s:%s' % (namespace, url_name), **kwars)
        else:
            return redirect(request.path)

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
