from django.db.models import F
from django.shortcuts import redirect as dj_redirect, render

from misago.core.shortcuts import get_object_or_404, validate_slug

from misago.forums.lists import get_forums_list, get_forum_path
from misago.forums.models import Forum
from misago.forums.permissions import allow_see_forum, allow_browse_forum


def forum_view(role):
    def wrap(f):
        def decorator(request, forum_slug, forum_id):
            allow_see_forum(request.user, forum_id)

            forums = Forum.objects.all_forums()
            forum = get_object_or_404(forums, pk=forum_id, role=role)
            validate_slug(forum, forum_slug)

            return f(request, forum)
        return decorator
    return wrap


@forum_view('category')
def category(request, forum):
    allow_browse_forum(request.user, forum)
    if forum.level == 1:
        return dj_redirect(forum.get_absolute_url())
    forums = get_forums_list(request.user, forum)

    return render(request, 'misago/forums/category.html', {
        'category': forum,
        'forums': forums,
        'path': get_forum_path(forum),
    })


@forum_view('redirect')
def redirect(request, forum):
    if forum.pk not in request.session.get('forum_redirects', []):
        request.session.setdefault('forum_redirects', []).append(forum.pk)
        forum.redirects_count = F('redirects_count') + 1
        forum.save(update_fields=['redirects_count'])
    return dj_redirect(forum.redirect_url)


@forum_view('-')
def forum(request, forum):
    pass
