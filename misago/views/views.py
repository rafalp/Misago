from django.shortcuts import render
from django.http import Http404


def forum_index(request):
    return render(request, 'misago/front/index.html')
