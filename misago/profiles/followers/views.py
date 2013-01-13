from misago.profiles.decorators import profile_view
from misago.profiles.template import RequestContext

@profile_view('user_followers')
def followers(request, user):
    return request.theme.render_to_response('profiles/profile.html',
                                            context_instance=RequestContext(request, {
                                             'profile': user,
                                             'tab': 'followers',
                                             }));