from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from misago.apps.profiles.decorators import profile_view
from misago.apps.profiles.template import RequestContext
from misago.utils.pagination import make_pagination

@profile_view('user_follows')
def follows(request, user, page=0):
    queryset = user.follows.order_by('username_slug')
    count = queryset.count()
    try:
        pagination = make_pagination(page, count, 24)
    except Http404:
        return redirect(reverse('user_follows', kwargs={'user': user.id, 'username': user.username_slug}))

    return request.theme.render_to_response('profiles/follows.html',
                                            context_instance=RequestContext(request, {
                                             'profile': user,
                                             'tab': 'follows',
                                             'items_total': count,
                                             'items': queryset[pagination['start']:pagination['stop']],
                                             'pagination': pagination,
                                             }));
