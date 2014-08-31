from misago.threads.models import Thread, Post
from misago.users.models import User, ACTIVATION_REQUIRED_NONE

from misago.admin.views import render


def admin_index(request):
    inactive_users = {'requires_activation__gt': ACTIVATION_REQUIRED_NONE}
    db_stats = {
        'threads': Thread.objects.count(),
        'posts': Post.objects.count(),
        'users': User.objects.count(),
        'inactive_users': User.objects.filter(**inactive_users)
    }

    return render(request, 'misago/admin/index.html', {
        'db_stats': db_stats,
    })
