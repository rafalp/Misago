from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago import messages
from misago.decorators import block_guest, check_csrf
from misago.models import ForumRead, ThreadRead

@block_guest
@check_csrf
def read_all(request):
    ForumRead.objects.filter(user=request.user).delete()
    ThreadRead.objects.filter(user=request.user).delete()
    now = timezone.now()
    bulk = []
    for forum in request.acl.forums.known_forums():
        new_record = ForumRead(user=request.user, forum_id=forum, updated=now, cleared=now)
        bulk.append(new_record)
    if bulk:
        ForumRead.objects.bulk_create(bulk)
    messages.success(request, _("All forums have been marked as read."))
    return redirect(reverse('index'))
