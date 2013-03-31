from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.apps.errors import error403, error404
from misago.forms import FormFields
from misago.messages import Message
from misago.models import Rank, User
from misago.utils.strings import slugify
from misago.utils.pagination import make_pagination
from misago.apps.profiles.forms import QuickFindUserForm

def list(request, slug=None, page=1):
    ranks = Rank.objects.filter(as_tab=1).order_by('order')

    # Find active rank
    default_rank = False
    active_rank = None
    if slug:
        for rank in ranks:
            if rank.slug == slug:
                active_rank = rank
        if not active_rank:
            return error404(request)
        if ranks and active_rank.slug == ranks[0].slug:
            return redirect(reverse('users'))
    elif ranks:
        default_rank = True
        active_rank = ranks[0]

    # Empty Defaults
    message = None
    users = []
    items_total = 0
    pagination = None
    in_search = False

    # Users search?
    if request.method == 'POST':
        if not request.acl.users.can_search_users():
            return error403(request)
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
                users = User.objects.filter(username_slug__startswith=username).order_by('username_slug')[:10]
        elif search_form.non_field_errors()[0] == 'form_contains_errors':
            message = Message(_("To search users you have to enter username in search field."), 'error')
        else:
            message = Message(search_form.non_field_errors()[0], 'error')
    else:
        search_form = QuickFindUserForm(request=request)
        if active_rank:
            users = User.objects.filter(rank=active_rank)
            items_total = users.count()
            pagination = make_pagination(page, items_total, request.settings['profiles_per_list'])
            users = users.order_by('username_slug')[pagination['start']:pagination['stop']]

    return request.theme.render_to_response('profiles/list.html',
                                        {
                                         'message': message,
                                         'search_form': FormFields(search_form).fields,
                                         'in_search': in_search,
                                         'active_rank': active_rank,
                                         'default_rank': default_rank,
                                         'items_total': items_total,
                                         'ranks': ranks,
                                         'users': users,
                                         'pagination': pagination,
                                        },
                                        context_instance=RequestContext(request));