from datetime import timedelta
from django.template import RequestContext
from django.utils import timezone
from misago.models import Thread
from misago.utils.pagination import make_pagination

def popular_threads(request, page=0):
    queryset = Thread.objects.filter(forum_id__in=request.acl.threads.get_readable_forums(request.acl)).filter(deleted=False).filter(moderated=False)
    items_total = queryset.count();
    pagination = make_pagination(page, items_total, 30)

    queryset = queryset.order_by('-score').prefetch_related('forum')[pagination['start']:pagination['stop']];
    if request.settings['avatars_on_threads_list']:
        queryset = queryset.prefetch_related('start_poster', 'last_poster')

    return request.theme.render_to_response('popular_threads.html',
                                            {
                                             'items_total': items_total,
                                             'threads': Thread.objects.with_reads(queryset, request.user),
                                             'pagination': pagination,
                                             },
                                            context_instance=RequestContext(request));