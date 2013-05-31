from datetime import timedelta
from django.core.cache import cache
from django.template import RequestContext
from django.utils import timezone
from misago.models import Forum, Post, Rank, Session, Thread
from misago.readstrackers import ForumsTracker

def index(request):
    # Threads ranking
    popular_threads = []
    if request.settings['thread_ranking_size'] > 0:
        popular_threads = cache.get('thread_ranking_%s' % request.user.make_acl_key(), 'nada')
        if popular_threads == 'nada':
            popular_threads = []
            for thread in Thread.objects.filter(moderated=False).filter(deleted=False).filter(forum__in=Forum.objects.readable_forums(request.acl)).prefetch_related('forum').order_by('-score')[:request.settings['thread_ranking_size']]:
                thread.forum_name = thread.forum.name
                thread.forum_slug = thread.forum.slug
                popular_threads.append(thread)
            cache.set('thread_ranking_%s' % request.user.make_acl_key(), popular_threads, 60 * request.settings['thread_ranking_refresh'])

    # Users online
    users_online = request.onlines.stats(request)

    # Ranks online
    ranks_list = cache.get('ranks_online', 'nada')
    if ranks_list == 'nada':
        ranks_dict = {}
        ranks_list = []
        users_list = []
        for rank in Rank.objects.filter(on_index=True).order_by('order'):
            rank_entry = {
                          'id':rank.id,
                          'name': rank.name,
                          'slug': rank.slug if rank.as_tab else '',
                          'style': rank.style,
                          'title': rank.title,
                          'online': [],
                          'pks': [],
                         }
            ranks_list.append(rank_entry)
            ranks_dict[rank.pk] = rank_entry
        if ranks_dict:
            for session in Session.objects.select_related('user').filter(rank__in=ranks_dict.keys()).filter(last__gte=timezone.now() - timedelta(seconds=request.settings['online_counting_frequency'])).filter(user__isnull=False):
                if not session.user_id in users_list:
                    ranks_dict[session.user.rank_id]['online'].append(session.user)
                    ranks_dict[session.user.rank_id]['pks'].append(session.user.pk)
                    users_list.append(session.user_id)
            # Assert we are on list
            if (request.user.is_authenticated() and request.user.rank_id in ranks_dict.keys()
                and not request.user.pk in users_list):
                    ranks_dict[request.user.rank_id]['online'].append(request.user)
                    ranks_dict[request.user.rank_id]['pks'].append(request.user.pk)
                    users_list.append(request.user.pk)
            cache.set('team_users_online', users_list, request.settings['online_counting_frequency'])
            del ranks_dict
            del users_list
        cache.set('ranks_online', ranks_list, request.settings['online_counting_frequency'])
    elif request.user.is_authenticated():
        for rank in ranks_list:
            if rank['id'] == request.user.rank_id and not request.user.pk in rank['pks']:
                rank['online'].append(request.user)
                rank['pks'].append(request.user.pk)
                break

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
