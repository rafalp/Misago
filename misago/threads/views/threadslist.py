from django.shortcuts import render


def threads_list(request):
    return render(request, 'misago/threadslist/threads.html')