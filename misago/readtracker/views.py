from django.contrib import messages
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from misago.core.decorators import require_POST
from misago.forums.models import Forum
from misago.users.decorators import deny_guests

from misago.readtracker import forumstracker
from misago.readtracker.signals import all_read


def read_view(f):
    @deny_guests
    @require_POST
    @csrf_protect
    @never_cache
    @atomic
    def decorator(request, *args, **kwargs):
        return f(request, *args, **kwargs)
    return decorator


@read_view
def read_all(request):
    request.user.reads_cutoff = timezone.now()
    request.user.save(update_fields=['reads_cutoff'])

    all_read.send(sender=request.user)

    messages.info(request, _("All forums and threads were marked as read."))
    return redirect('misago:index')


@read_view
def read_forum(request, forum_id):
    forum = get_object_or_404(Forum.objects, id=forum_id)
    forumstracker.read_forum(request.user, forum)

    messages.info(request, _("Threads were marked as read."))
    return redirect(forum.get_absolute_url())
