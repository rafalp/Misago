import floppyforms as forms
from django.core.urlresolvers import reverse
from django.db.models import Q, F
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.apps.errors import error403
from misago.conf import settings
from misago.decorators import block_guest
from misago.forms import Form, FormLayout, FormFields
from misago.messages import Message
from misago.models import Forum, WatchedThread
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination

@block_guest
def watched_threads(request, page=0, new=False):
    # Find mode and fetch threads
    readable_forums = Forum.objects.readable_forums(request.acl, True)
    starter_readable_forums = Forum.objects.starter_readable_forums(request.acl)

    if not readable_forums and not readable_forums:
        return error403(request, _("%(username), you cannot read any forums.") % {'username': request.user.username})

    private_threads_pk = Forum.objects.special_pk('private_threads')
    if not settings.enable_private_threads and private_threads_pk in readable_forums:
        readable_forums.remove(private_threads_pk)

    queryset = WatchedThread.objects.filter(user=request.user).filter(thread__moderated=False).filter(thread__deleted=False).select_related('thread')
    if starter_readable_forums and readable_forums:
        queryset = queryset.filter(Q(forum_id__in=readable_forums) | Q(forum_id__in=starter_readable_forums, starter_id=request.user.pk))
    elif starter_readable_forums:
        queryset = queryset.filter(starter_id__in=request.user.pk).filter(forum_id__in=starter_readable_forums)
    else:
        queryset = queryset.filter(forum_id__in=readable_forums)

    if settings.avatars_on_threads_list:
        queryset = queryset.prefetch_related('thread__last_poster')
    if new:
        queryset = queryset.filter(last_read__lt=F('thread__last'))
    count = queryset.count()
    try:
        pagination = make_pagination(page, count, settings.threads_per_page)
    except Http404:
        if new:
            return redirect(reverse('watched_threads_new'))
        return redirect(reverse('watched_threads'))
    queryset = queryset.order_by('-thread__last')
    if settings.threads_per_page < count:
        queryset = queryset[pagination['start']:pagination['stop']]
    queryset.prefetch_related('thread__forum', 'thread__start_poster', 'thread__last_poster')
    threads = []
    for thread in queryset:
        thread.thread.send_email = thread.email
        thread.thread.is_read = thread.thread.last <= thread.last_read             
        threads.append(thread.thread)
            
    # Display page
    return render_to_response('watched.html',
                              {
                              'items_total': count,
                              'pagination': pagination,
                              'new': new,
                              'threads': threads,
                              'message': request.messages.get_message('threads'),
                              },
                              context_instance=RequestContext(request))