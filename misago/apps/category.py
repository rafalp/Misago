from django.template import RequestContext
from misago.apps.errors import error403, error404
from misago.models import Forum
from misago.readstrackers import ForumsTracker

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
                                             'parents': Forum.objects.forum_parents(forum.pk),
                                             },
                                            context_instance=RequestContext(request));