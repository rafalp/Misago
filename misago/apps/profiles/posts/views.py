from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from misago.apps.profiles.decorators import profile_view
from misago.apps.profiles.template import RequestContext
from misago.models import Forum
from misago.utils.pagination import make_pagination

@profile_view('user_posts')
def posts(request, user, page=0):
    queryset = user.post_set.filter(forum_id__in=Forum.objects.readable_forums(request.acl)).filter(deleted=False).filter(moderated=False).select_related('thread', 'forum').order_by('-id')
    count = queryset.count()
    try:
        pagination = make_pagination(page, count, 12)
    except Http404:
        return redirect(reverse('user_posts', kwargs={'user': user.id, 'username': user.username_slug}))
    
    return request.theme.render_to_response('profiles/posts.html',
                                            context_instance=RequestContext(request, {
                                             'profile': user,
                                             'tab': 'posts',
                                             'items_total': count,
                                             'items': queryset[pagination['start']:pagination['stop']],
                                             'pagination': pagination,
                                             }));
