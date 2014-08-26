from django.shortcuts import render

from misago.acl import add_acl
from misago.forums.lists import get_forums_list
from misago.users.online.ranks import get_ranks_online


def forum_index(request):
    forums_list = get_forums_list(request.user)
    add_acl(request.user, forums_list)

    return render(request, 'misago/index.html', {
        'categories': forums_list,
        'ranks_online': get_ranks_online(request.user),
    })
