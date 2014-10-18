from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ungettext, ugettext_lazy, ugettext as _

from misago.acl import add_acl
from misago.forums.lists import get_forum_path
from misago.threads.models import Label
from misago.readtracker import threadstracker
from misago.users.online.utils import get_user_state

from misago.threads.events import add_events_to_posts
from misago.threads.paginator import paginate
from misago.threads.views.generic.actions import ActionsBase
from misago.threads.views.generic.base import ViewBase


__all__ = ['ThreadActions']


class ThreadActions(ActionsBase):
    query_key = 'thread_action'
    is_mass_action = False

    def get_available_actions(self, kwargs):
        self.thread = kwargs['thread']
        self.forum = self.thread.forum

        actions = []

        if self.forum.acl['can_change_threads_labels'] == 2:
            self.forum.labels = Label.objects.get_forum_labels(self.forum)
            for label in self.forum.labels:
                if label.pk != self.thread.label_id:
                    name = _('Label as "%(label)s"') % {'label': label.name}
                    actions.append({
                        'action': 'label:%s' % label.slug,
                        'icon': 'tag',
                        'name': name
                    })

            if self.forum.labels and self.thread.label_id:
                actions.append({
                    'action': 'unlabel',
                    'icon': 'times-circle',
                    'name': _("Remove label")
                })

        if self.forum.acl['can_pin_threads']:
            if self.thread.is_pinned:
                actions.append({
                    'action': 'unpin',
                    'icon': 'circle',
                    'name': _("Unpin thread")
                })
            else:
                actions.append({
                    'action': 'pin',
                    'icon': 'star',
                    'name': _("Pin thread")
                })

        if self.forum.acl['can_review_moderated_content']:
            if self.thread.is_moderated:
                actions.append({
                    'action': 'approve',
                    'icon': 'check',
                    'name': _("Approve thread")
                })

        if self.forum.acl['can_move_threads']:
            actions.append({
                'action': 'move',
                'icon': 'arrow-right',
                'name': _("Move thread")
            })

        if self.forum.acl['can_close_threads']:
            if self.thread.is_closed:
                actions.append({
                    'action': 'open',
                    'icon': 'unlock-alt',
                    'name': _("Open thread")
                })
            else:
                actions.append({
                    'action': 'close',
                    'icon': 'lock',
                    'name': _("Close thread")
                })

        if self.forum.acl['can_hide_threads']:
            if self.thread.is_hidden:
                actions.append({
                    'action': 'unhide',
                    'icon': 'eye',
                    'name': _("Unhide thread")
                })
            else:
                actions.append({
                    'action': 'hide',
                    'icon': 'eye-slash',
                    'name': _("Hide thread")
                })

        if self.forum.acl['can_hide_threads'] == 2:
            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete thread"),
                'confirmation': _("Are you sure you want to delete this "
                                  "thread? This action can't be undone.")
            })

        return actions


class PostsActions(ActionsBase):
    select_items_message = ugettext_lazy(
        "You have to select at least one post.")
    is_mass_action = True

    def get_available_actions(self, kwargs):
        return []


class ThreadView(ViewBase):
    """
    Basic view for threads
    """
    ThreadActions = ThreadActions
    PostsActions = PostsActions
    template = 'misago/thread/replies.html'

    def get_posts(self, user, forum, thread, kwargs):
        queryset = self.get_posts_queryset(user, forum, thread)
        page = paginate(queryset, kwargs.get('page', 0), 10, 5)

        posts = []
        for post in page.object_list:
            add_acl(user, post)
            if post.poster:
                poster_state = get_user_state(post.poster, user.acl)
                post.poster.online_state = poster_state
            posts.append(post)

        if page.next_page_first_item:
            add_events_to_posts(
                user, thread, posts, page.next_page_first_item.posted_on)
        else:
            add_events_to_posts(user, thread, posts)

        return page, posts

    def get_posts_queryset(self, user, forum, thread):
        queryset = thread.post_set.select_related(
            'poster', 'poster__rank', 'poster__bancache', 'poster__online')

        if user.is_authenticated():
            if forum.acl['can_review_moderated_content']:
                visibility_condition = Q(is_moderated=False) | Q(poster=user)
                queryset = queryset.filter(visibility_condition)
        else:
            queryset = queryset.filter(is_moderated=False)

        return queryset.order_by('id')

    def dispatch(self, request, *args, **kwargs):
        relations = ['forum', 'starter', 'last_poster', 'first_post']
        thread = self.fetch_thread(request, select_related=relations, **kwargs)
        forum = thread.forum

        self.check_forum_permissions(request, forum)
        self.check_thread_permissions(request, thread)

        threadstracker.make_read_aware(request.user, thread)

        thread_actions = self.ThreadActions(user=request.user, thread=thread)
        posts_actions = self.PostsActions(user=request.user, thread=thread)

        page, posts = self.get_posts(request.user, forum, thread, kwargs)
        threadstracker.make_posts_read_aware(request.user, thread, posts)
        threadstracker.read_thread(request.user, thread, posts[-1])

        return self.render(request, {
            'link_name': thread.get_url(),
            'links_params': {
                'thread_id': thread.id, 'thread_slug': thread.slug
            },

            'forum': forum,
            'path': get_forum_path(forum),

            'thread': thread,
            'thread_actions': thread_actions.get_list(),

            'posts': posts,
            'posts_actions': posts_actions.get_list(),

            'paginator': page.paginator,
            'page': page,
        })
