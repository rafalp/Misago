from misago.profiles.decorators import profile_view
from misago.profiles.template import RequestContext
from misago.utils import make_pagination

@profile_view('user_followers')
def followers(request, user, page=0):
    queryset = user.follows_set.order_by('username_slug')
    count = queryset.count()
    pagination = make_pagination(page, count, 40)
    return request.theme.render_to_response('profiles/followers.html',
                                            context_instance=RequestContext(request, {
                                             'profile': user,
                                             'tab': 'followers',
                                             'items_total': count,
                                             'items': queryset[pagination['start']:pagination['stop']],
                                             'pagination': pagination,
                                             }));