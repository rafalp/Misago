from django.shortcuts import redirect
from misago.admin.views import render


def index(request):
    return render(request, 'misago/admin/conf/index.html')
