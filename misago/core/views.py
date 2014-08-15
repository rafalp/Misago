from django.shortcuts import render

from misago.forums.lists import get_forums_list

from misago.users.online.ranks import get_ranks_online


def forum_index(request):
    return render(request, 'misago/index.html', {
        'categories': get_forums_list(request.user),
        'ranks_online': get_ranks_online(request.user),
    })
