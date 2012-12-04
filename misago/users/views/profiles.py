from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.users.models import User
from misago.views import error404


def profile(request, user, username, tab='posts'):
    user = int(user)
    try:
        user = User.objects.get(pk=user)
        if user.username_slug != username:
            # Force crawlers to take notice of updated username
            return redirect(reverse('user', args=(user.username_slug, user.pk)), permanent=True)
        return globals()['profile_%s' % tab](request, user)
    except User.DoesNotExist:
        return error404(request)
    

def profile_posts(request, user):
    return request.theme.render_to_response('users/profile/profile.html',
                                            {
                                             'profile': user,
                                             'tab': 'posts',
                                            },
                                            context_instance=RequestContext(request));
    

def profile_threads(request, user):
    return request.theme.render_to_response('users/profile/profile.html',
                                            {
                                             'profile': user,
                                             'tab': 'threads',
                                            },
                                            context_instance=RequestContext(request));
    

def profile_following(request, user):
    return request.theme.render_to_response('users/profile/profile.html',
                                            {
                                             'profile': user,
                                             'tab': 'following',
                                            },
                                            context_instance=RequestContext(request));
    

def profile_followers(request, user):
    return request.theme.render_to_response('users/profile/profile.html',
                                            {
                                             'profile': user,
                                             'tab': 'followers',
                                            },
                                            context_instance=RequestContext(request));
    

def profile_details(request, user):
    return request.theme.render_to_response('users/profile/details.html',
                                            {
                                             'profile': user,
                                             'tab': 'details',
                                            },
                                            context_instance=RequestContext(request));