from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403
from misago.apps.errors import error403, error404
from misago.decorators import block_guest, check_csrf
from misago.models import Forum, User

@block_guest
@check_csrf
def destroy_user(request, user, username):
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return error404(request)

    if user.pk == request.user.pk:
        return error403(request, _("You can't destroy your own account."))

    try:
        request.acl.destroyusers.allow_destroy_user(user)
    except ACLError403 as e:
        return error403(request, unicode(e))

    forums_to_sync = []

    for thread in user.thread_set.iterator():
        if not thread.forum_id in forums_to_sync:
            forums_to_sync.append(thread.forum_id)
        thread.delete()

    if forums_to_sync:
        for forum in Forum.objects.filter(id__in=forums_to_sync).iterator():
            forum.sync()
            forum.save()

    user.post_set.update(deleted=True)
    user.delete()

    messages.success(request, _('User Account "%(username)s" has been destroyed.') % {'username': user.username})
    return redirect('users')
