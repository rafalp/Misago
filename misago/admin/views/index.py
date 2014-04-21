from misago.admin.views import render


def admin_index(request):
    return render(request, 'misago/admin/index.html')
