from datetime import timedelta
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403
from misago.apps.errors import error403, error404
from misago.apps.warnuser.forms import WarnMemberForm
from misago.decorators import block_guest, check_csrf
from misago.models import User, Warn, WarnLevel
from misago.shortcuts import render_to_response

@block_guest
@check_csrf
def warn_user(request, user, slug):
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return error404(request, _("Requested user could not be found."))

    try:
        request.acl.warnings.allow_warning_members()
        user.acl().warnings.allow_warning()
    except ACLError403 as e:
        return error403(request, e)

    if not WarnLevel.objects.get_level(1):
        messages.error(request, _("No warning levels have been defined."))
        return redirect(request.POST.get('retreat',
            reverse('user', kwargs={
                'user': user.pk,
                'username': user.username_slug,
                })))

    current_warning_level = user.get_current_warning_level()
    next_warning_level = WarnLevel.objects.get_level(user.warning_level + 1)

    if not next_warning_level:
        return render_to_response('warn_user/max_level.html',
                                  {
                                   'warned_user': user,
                                   'retreat': request.POST.get('retreat'),
                                  },
                                  context_instance=RequestContext(request))

    form = WarnMemberForm(initial={'reason': request.POST.get('reason')})
    if ('origin' in request.POST
            and request.POST.get('origin') == 'warning-form'):
        form = WarnMemberForm(request.POST, request=request)
        if form.is_valid():
            user.warning_level += 1
            if next_warning_level.expires_after_minutes:
                user.warning_level_update_on = timezone.now()
                user.warning_level_update_on += timedelta(
                    minutes=next_warning_level.expires_after_minutes)
            else:
                user.warning_level_update_on = None
            user.save(force_update=True)

            Warn.objects.create(
                user=user,
                giver=request.user,
                giver_name=request.user.username,
                giver_slug=request.user.username_slug,
                date=timezone.now(),
                ip=request.session.get_ip(request),
                agent=request.META.get('HTTP_USER_AGENT'),
                reason=form.cleaned_data['reason'],
                )

            messages.success(request,
                _("%(user)s warning level has been increased.") % {
                    'user': user.username})
            return redirect(request.POST.get('retreat',
                reverse('user', kwargs={
                    'user': user.pk,
                    'username': user.username_slug,
                    })))

    return render_to_response('warn_user/form.html',
                              {
                               'warned_user': user,
                               'current_warning_level': current_warning_level,
                               'next_warning_level': next_warning_level,
                               'form': form,
                               'retreat': request.POST.get('retreat'),
                              },
                              context_instance=RequestContext(request))
