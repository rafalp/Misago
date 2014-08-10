from django.shortcuts import render

from misago.users.online.ranks import get_ranks_online


def forum_index(request):
    return render(request, 'misago/index.html', {
        'ranks_online': get_ranks_online()
    })
