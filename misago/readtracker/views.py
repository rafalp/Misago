from django.contrib import messages
from django.db.transaction import atomic
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from misago.core.decorators import require_POST
from misago.users.decorators import deny_guests

from misago.readtracker.signals import all_read


@deny_guests
@require_POST
@csrf_protect
@never_cache
@atomic
def read_all(request):
    request.user.reads_cutoff = timezone.now()
    request.user.save(update_fields=['reads_cutoff'])

    all_read.send(sender=request.user)

    messages.info(request, _("All forums and threads were marked as read."))
    return redirect('misago:index')
