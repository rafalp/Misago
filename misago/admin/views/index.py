from misago.admin.views import render


def admin_index(request):
    namespace = request.resolver_match.namespace
    return render(request, 'misago/admin/index.html', {'namespace': namespace})
