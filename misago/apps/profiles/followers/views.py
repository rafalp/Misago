from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from misago.apps.profiles.decorators import profile_view
from misago.apps.profiles.template import RequestContext
from misago.utils.pagination import make_pagination

@profile_view('user_followers')
def followers(request, user, page=0):
    queryset = user.follows_set.order_by('username_slug')
    count = queryset.count()
    try:
        pagination = make_pagination(page, count, 24)
    except Http404:
        return redirect(reverse('user_followers', kwargs={'user': user.id, 'username': user.username_slug}))
    
    return request.theme.render_to_response('profiles/followers.html',
                                            context_instance=RequestContext(request, {
                                             'profile': user,
                                             'tab': 'followers',
                                             'items_total': count,
                                             'items': queryset[pagination['start']:pagination['stop']],
                                             'pagination': pagination,
                                             }));