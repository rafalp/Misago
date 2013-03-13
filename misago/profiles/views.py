from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.forms import FormFields
from misago.messages import Message
from misago.profiles.forms import QuickFindUserForm
from misago.ranks.models import Rank
from misago.users.models import User
from misago.utils import slugify, make_pagination
from misago.views import error403, error404

def list(request, rank_slug=None, page=1):
    ranks = Rank.objects.filter(as_tab=1).order_by('order')

    # Find active rank
    default_rank = False
    active_rank = None
    if rank_slug:
        for rank in ranks:
            if rank.name_slug == rank_slug:
                active_rank = rank
        if not active_rank:
            return error404(request)
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
            count = users.count()
            pagination = make_pagination(page, count, 4)
            users = users.order_by('username_slug')[pagination['start']:pagination['stop']]

    return request.theme.render_to_response('profiles/list.html',
                                        {
                                         'message': message,
                                         'search_form': FormFields(search_form).fields,
                                         'in_search': in_search,
                                         'active_rank': active_rank,
                                         'default_rank': default_rank,
                                         'items_total': count,
                                         'ranks': ranks,
                                         'users': users,
                                         'pagination': pagination,
                                        },
                                        context_instance=RequestContext(request));