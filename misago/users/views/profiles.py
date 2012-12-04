from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.forms import FormFields
from misago.messages import Message
from misago.ranks.models import Rank
from misago.users.forms import QuickFindUserForm
from misago.users.models import User
from misago.views import error404
from misago.utils import slugify


def list(request, rank_slug=None):
    ranks = Rank.objects.filter(as_tab=1).order_by('order')
    
    # Find active rank
    active_rank = None
    if rank_slug:
        for rank in ranks:
            if rank.name_slug == rank_slug:
                active_rank = rank
        if not active_rank:
            return error404(request)
    elif ranks:
        active_rank = ranks[0]
    
    # Empty Defaults
    message = None
    users = []
    in_search = False
    
    # Users search?
    if request.method == 'POST':
        in_search = True
        active_rank = None
        search_form = QuickFindUserForm(request.POST, request=request)
        if search_form.is_valid():
            # Direct hit?
            username = search_form.cleaned_data['username']
            try:
                user = User.objects.get(username__iexact=username)
                return redirect(reverse('user', args=(user.username_slug, user.pk)))
            except User.DoesNotExist:
                pass
            
            # Looks like well have to find near match
            if len(username) > 6:
                username = username[0:-3]
            elif len(username) > 5:
                username = username[0:-2]
            elif len(username) > 4:
                username = username[0:-1]
            username = slugify(username.strip())
            
            # Go for rought match
            if len(username) > 0:
                print username
                users = User.objects.filter(username_slug__startswith=username).order_by('username_slug')[:10]
        elif search_form.non_field_errors()[0] == 'form_contains_errors':
            message = Message(_("To search users you have to enter username in search field."), 'error')
        else:
            message = Message(search_form.non_field_errors()[0], 'error')
    else:
        search_form = QuickFindUserForm(request=request)
        if active_rank:
            users = User.objects.filter(rank=active_rank).order_by('username_slug')
    
    return request.theme.render_to_response('users/list.html',
                                        {
                                         'message': message,
                                         'search_form': FormFields(search_form).fields,
                                         'in_search': in_search,
                                         'active_rank': active_rank,
                                         'ranks': ranks,
                                         'users': users,
                                        },
                                        context_instance=RequestContext(request));


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