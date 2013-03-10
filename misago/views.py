from datetime import timedelta
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.csrf.decorators import check_csrf
from misago.forums.models import Forum
from misago.messages import Message
from misago.readstracker.models import Record
from misago.readstracker.trackers import ForumsTracker
from misago.ranks.models import Rank
from misago.sessions.models import Session
from misago.threads.models import Thread

def home(request):
    # Threads ranking
    popular_threads = []
    if request.settings['thread_ranking_size'] > 0:
        popular_threads = cache.get('thread_ranking_%s' % request.user.make_acl_key(), 'nada')
        if popular_threads == 'nada':
            popular_threads = []
            for thread in Thread.objects.filter(moderated=False).filter(deleted=False).filter(forum__in=request.acl.threads.get_readable_forums(request.acl)).prefetch_related('forum').order_by('-score')[:request.settings['thread_ranking_size']]:
                thread.forum_name = thread.forum.name
                thread.forum_slug = thread.forum.slug
                popular_threads.append(thread)
            cache.set('thread_ranking_%s' % request.user.make_acl_key(), popular_threads, 60 * request.settings['thread_ranking_refresh'])

    # Ranks online
    ranks_list = cache.get('ranks_online', 'nada')
    if ranks_list == 'nada':
        ranks_dict = {}
        ranks_list = []
        users_list = []
        for rank in Rank.objects.filter(on_index=True).order_by('order'):
            rank_entry = {'name': rank.name, 'style': rank.style, 'title': rank.title, 'online': []}
            ranks_list.append(rank_entry)
            ranks_dict[rank.pk] = rank_entry
        if ranks_dict:
            for session in Session.objects.select_related('user').filter(rank__in=ranks_dict.keys()).filter(last__gte=timezone.now() - timedelta(minutes=10)).filter(user__isnull=False):
                if not session.user_id in users_list:
                    ranks_dict[session.user.rank_id]['online'].append(session.user)
                    users_list.append(session.user_id)
            del ranks_dict
            del users_list
        cache.set('ranks_online', ranks_list, 300)

    # Users online
    users_online = cache.get('users_online', 'nada')
    if users_online == 'nada':
        users_online = Session.objects.filter(matched=True).filter(crawler__isnull=True).filter(last__gte=timezone.now() - timedelta(seconds=300)).count()
        cache.set('users_online', users_online, 300)
    if not users_online and not request.user.is_crawler():
        # Cheatey trick to make sure we'll never display
        # zero users online to human client
        users_online = 1

    # Load reads tracker and build forums list
    reads_tracker = ForumsTracker(request.user)
    forums_list = Forum.objects.treelist(request.acl.forums, tracker=reads_tracker)
    
    # Whitelist ignored members
    Forum.objects.ignored_users(request.user, forums_list)
        
    # Render page 
    return request.theme.render_to_response('index.html',
                                            {
                                             'forums_list': forums_list,
                                             'ranks_online': ranks_list,
                                             'users_online': users_online,
                                             'popular_threads': popular_threads,
                                             },
                                            context_instance=RequestContext(request));


def category(request, forum, slug):
    if not request.acl.forums.can_see(forum):
        return error404(request)
    try:
        forum = Forum.objects.get(pk=forum, type='category')
        if not request.acl.forums.can_browse(forum):
            return error403(request, _("You don't have permission to browse this category."))
    except Forum.DoesNotExist:
        return error404(request)

    forum.subforums = Forum.objects.treelist(request.acl.forums, forum, tracker=ForumsTracker(request.user))
    return request.theme.render_to_response('category.html',
                                            {
                                             'category': forum,
                                             'parents': Forum.objects.forum_parents(forum.pk),
                                             },
                                            context_instance=RequestContext(request));


def redirection(request, forum, slug):
    if not request.acl.forums.can_see(forum):
        return error404(request)
    try:
        forum = Forum.objects.get(pk=forum, type='redirect')
        if not request.acl.forums.can_browse(forum):
            return error403(request, _("You don't have permission to follow this redirect."))
        redirects_tracker = request.session.get('redirects', [])
        if forum.pk not in redirects_tracker:
            redirects_tracker.append(forum.pk)
            request.session['redirects'] = redirects_tracker
            forum.redirects += 1
            forum.save(force_update=True)
        return redirect(forum.redirect)
    except Forum.DoesNotExist:
        return error404(request)


@block_guest
@check_csrf
def read_all(request):
    Record.objects.filter(user=request.user).delete()
    now = timezone.now()
    bulk = []
    for forum in request.acl.forums.known_forums():
        new_record = Record(user=request.user, forum_id=forum, updated=now, cleared=now)
        new_record.set_threads({})
        bulk.append(new_record)
    if bulk:
        Record.objects.bulk_create(bulk)
    request.messages.set_flash(Message(_("All forums have been marked as read.")), 'success')
    return redirect(reverse('index'))


def forum_map(request):
    return request.theme.render_to_response('forum_map.html',
                                            {
                                             'ranks': Rank.objects.filter(as_tab=1).order_by('order'),
                                             'forums': Forum.objects.treelist(request.acl.forums),
                                             },
                                            context_instance=RequestContext(request));


def popular_threads(request):
    return request.theme.render_to_response('popular_threads.html',
                                            {
                                             'threads': Thread.objects.filter(forum_id__in=request.acl.threads.get_readable_forums(request.acl)).filter(deleted=False).filter(moderated=False).order_by('-score').prefetch_related('start_poster', 'last_poster', 'forum')[:50],
                                             },
                                            context_instance=RequestContext(request));


def redirect_message(request, message, type='info', owner=None):
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


def error403(request, message=None):
    return error_view(request, 403, message)


def error404(request, message=None):
    return error_view(request, 404, message)


def error_view(request, error, message):
    response = request.theme.render_to_response(('error%s.html' % error),
                                                {
                                                 'message': message,
                                                 'hide_signin': True,
                                                 'exception_response': True,
                                                 },
                                                context_instance=RequestContext(request));
    response.status_code = error
    return response
