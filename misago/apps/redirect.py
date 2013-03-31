from django.shortcuts import redirect as django_redirect
from django.utils.translation import ugettext as _
from misago.apps.errors import error403, error404
from misago.models import Forum

def redirect(request, forum, slug):
    if not request.acl.forums.can_see(forum):
        return error404(request)
    try:
        forum = Forum.objects.get(pk=forum, type='redirect')
        if not request.acl.forums.can_browse(forum):
            return error403(request, _("You don't have permission to follow this redirect."))
        redirects_tracker = request.session.get('redirects', [])
        if forum.pk not in redirects_tracker:
            redirects_tracker.append(forum.pk)
            request.session['redirects'] = redirects_tracker
            forum.redirects += 1
            forum.save(force_update=True)
        return django_redirect(forum.redirect)
    except Forum.DoesNotExist:
        return error404(request)