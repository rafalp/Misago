from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forums.models import Forum
from misago.readstracker.trackers import ForumsTracker
from misago.sessions.models import Session

def home(request):
    team_online = []
    team_pks = []
    for session in Session.objects.filter(team=1).filter(admin=0).filter(user__isnull=False).order_by('-start').select_related('user', 'user__rank'):
        if session.user.pk not in team_pks:
            team_pks.append(session.user.pk)
            team_online.append(session.user)
    reads_tracker = ForumsTracker(request.user)
    return request.theme.render_to_response('index.html',
                                            {
                                             'forums_list': Forum.objects.treelist(request.acl.forums, tracker=reads_tracker),
                                             'team_online': team_online,
                                             },
                                            context_instance=RequestContext(request));


def category(request, forum, slug):
    if not request.acl.forums.can_see(forum):
        return error404(request)
    try:
        forum = Forum.objects.get(pk=forum, type='category')
        if not request.acl.forums.can_browse(forum):
            return error403(request, _("You don't have permission to browse this category."))
    except Forum.DoesNotExist:
        return error404(request)

    forum.subforums = Forum.objects.treelist(request.acl.forums, forum, tracker=ForumsTracker(request.user))
    return request.theme.render_to_response('category.html',
                                            {
                                             'category': forum,
                                             'parents': forum.get_ancestors().filter(level__gt=1),
                                             },
                                            context_instance=RequestContext(request));


def redirection(request, forum, slug):
    if not request.acl.forums.can_see(forum):
        return error404(request)
    try:
        forum = Forum.objects.get(pk=forum, type='redirect')
        if not request.acl.forums.can_browse(forum):
            return error403(request, _("You don't have permission to follow this redirect."))
        forum.redirects += 1
        forum.redirects_delta += 1
        forum.save(force_update=True)
        return redirect(forum.redirect)
    except Forum.DoesNotExist:
        return error404(request)


def redirect_message(request, message, type='info', owner=None):
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


def error403(request, message=None):
    return error_view(request, 403, message)

                                            
def error404(request, message=None):
    return error_view(request, 404, message)


def error_view(request, error, message):
    response = request.theme.render_to_response(('error%s.html' % error),
                                                {
                                                 'message': message,
                                                 'hide_signin': True,
                                                 'exception_response': True,
                                                 },
                                                context_instance=RequestContext(request));
    response.status_code = error
    return response