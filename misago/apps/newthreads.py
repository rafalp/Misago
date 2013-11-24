from datetime import timedelta
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from misago.conf import settings
from misago.models import Forum, Thread, ThreadPrefix
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination

def new_threads(request, page=0):
    queryset = Thread.objects.filter(forum_id__in=Forum.objects.readable_forums(request.acl)).filter(deleted=False).filter(moderated=False)
    items_total = queryset.count();
    if items_total > (settings.threads_per_page * 3):
        items_total = settings.threads_per_page * 3
    try:
        pagination = make_pagination(page, items_total, settings.threads_per_page)
    except Http404:
        return redirect(reverse('new_threads'))

    queryset = queryset.order_by('-start').prefetch_related('forum')[pagination['start']:pagination['stop']];
    if settings.avatars_on_threads_list:
        queryset = queryset.prefetch_related('start_poster', 'last_poster')

    return render_to_response('new_threads.html',
                              {
                              'items_total': items_total,
                              'threads': Thread.objects.with_reads(queryset, request.user),
                              'prefixes': ThreadPrefix.objects.all_prefixes(),
                              'pagination': pagination,
                              },
                              context_instance=RequestContext(request));