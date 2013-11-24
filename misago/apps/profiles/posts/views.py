from datetime import timedelta
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from misago.apps.profiles.decorators import profile_view
from misago.apps.profiles.template import RequestContext
from misago.models import Forum
from misago.shortcuts import render_to_response
from misago.utils.pagination import make_pagination

@profile_view('user_posts')
def posts(request, user, page=0):
    queryset = user.post_set.filter(forum_id__in=Forum.objects.readable_forums(request.acl)).filter(deleted=False).filter(moderated=False)
    count = queryset.count()
    try:
        pagination = make_pagination(page, count, 12)
    except Http404:
        return redirect(reverse('user_posts', kwargs={'user': user.id, 'username': user.username_slug}))
    
    cache_key = 'user_profile_posts_graph_%s' % user.pk
    graph = cache.get(cache_key, 'nada')
    if graph == 'nada':
        if user.posts:
            graph = user.timeline(queryset.filter(date__gte=timezone.now()-timedelta(days=100)))
        else:
            graph = [0 for x in range(100)]
        cache.set(cache_key, graph, 14400)

    return render_to_response('profiles/posts.html',
                              context_instance=RequestContext(request, {
                                  'profile': user,
                                  'tab': 'posts',
                                  'graph_max': max(graph),
                                  'graph': (str(i) for i in graph),
                                  'items_total': count,
                                  'items': queryset.select_related('thread', 'forum').order_by('-id')[pagination['start']:pagination['stop']],
                                  'pagination': pagination,
                                  }));
