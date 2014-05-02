from django.contrib import messages
from misago.admin.views import render


def admin_index(request):
    messages.success(request, 'Hello bro, I hope ya liking Miasgo!')
    namespace = request.resolver_match.namespace
    return render(request, 'misago/admin/index.html', {'namespace': namespace})
