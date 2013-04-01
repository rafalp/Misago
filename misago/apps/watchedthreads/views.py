from django import forms
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.decorators import block_guest
from misago.forms import Form, FormLayout, FormFields
from misago.messages import Message
from misago.models import Forum, WatchedThread
from misago.utils.pagination import make_pagination

@block_guest
def watched_threads(request, page=0, new=False):
    # Find mode and fetch threads
    readable_forums = Forum.objects.readable_forums(request.acl, True)
    if not request.settings['enable_private_threads']:
        readable_forums.remove(Forum.objects.special_pk('private_threads'))
    queryset = WatchedThread.objects.filter(user=request.user).filter(forum_id__in=readable_forums).select_related('thread').filter(thread__moderated=False).filter(thread__deleted=False)
    if new:
        queryset = queryset.filter(last_read__lt=F('thread__last'))
    count = queryset.count()
    pagination = make_pagination(page, count, request.settings.threads_per_page)
    queryset = queryset.order_by('-thread__last')
    if request.settings.threads_per_page < count:
        queryset = queryset[pagination['start']:pagination['stop']]
    queryset.prefetch_related('thread__forum', 'thread__start_poster', 'thread__last_poster')
    threads = []
    for thread in queryset:
        thread.thread.send_email = thread.email
        thread.thread.is_read = thread.thread.last <= thread.last_read             
        threads.append(thread.thread)
            
    # Display page
    return request.theme.render_to_response('watched.html',
                                            {
                                             'items_total': count,
                                             'pagination': pagination,
                                             'new': new,
                                             'threads': threads,
                                             'message': request.messages.get_message('threads'),
                                             },
                                            context_instance=RequestContext(request))