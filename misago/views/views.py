from django.shortcuts import render


def forum_index(request):
    return render(request, 'misago/front/index.html')
