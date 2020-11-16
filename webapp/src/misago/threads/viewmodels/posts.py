from ...acl.objectacl import add_acl_to_obj
from ...core.shortcuts import paginate, pagination_dict
from ...readtracker.poststracker import make_read_aware
from ...users.online.utils import make_users_status_aware
from ..paginator import PostsPaginator
from ..permissions import exclude_invisible_posts
from ..serializers import PostSerializer
from ..utils import add_likes_to_posts

__all__ = ["ThreadPosts"]


class ViewModel:
    def __init__(self, request, thread, page):  # pylint: disable=too-many-locals
        try:
            thread_model = thread.unwrap()
        except AttributeError:
            thread_model = thread

        posts_queryset = self.get_posts_queryset(request, thread_model)

        posts_limit = request.settings.posts_per_page
        posts_orphans = request.settings.posts_per_page_orphans
        list_page = paginate(
            posts_queryset, page, posts_limit, posts_orphans, paginator=PostsPaginator
        )
        paginator = pagination_dict(list_page)

        posts = list(list_page.object_list)
        posters = []

        for post in posts:
            post.category = thread.category
            post.thread = thread_model

            if post.poster:
                posters.append(post.poster)

        make_users_status_aware(request, posters)

        if thread.category.acl["can_see_posts_likes"]:
            add_likes_to_posts(request.user, posts)

        # add events to posts
        if thread_model.has_events:
            first_post = None
            if list_page.has_previous():
                first_post = posts[0]
            last_post = None
            if list_page.has_next():
                last_post = posts[-1]

            events_limit = request.settings.events_per_page
            posts += self.get_events_queryset(
                request, thread_model, events_limit, first_post, last_post
            )

            # sort both by pk
            posts.sort(key=lambda p: p.pk)

        # make posts and events ACL and reads aware
        add_acl_to_obj(request.user_acl, posts)
        make_read_aware(request, posts)

        self._user = request.user

        self.posts = posts
        self.paginator = paginator

    def get_posts_queryset(self, request, thread):
        queryset = (
            thread.post_set.select_related(
                "category",
                "poster",
                "poster__rank",
                "poster__ban_cache",
                "poster__online_tracker",
            )
            .filter(is_event=False)
            .order_by("id")
        )
        return exclude_invisible_posts(request.user_acl, thread.category, queryset)

    def get_events_queryset(
        self, request, thread, limit, first_post=None, last_post=None
    ):
        queryset = thread.post_set.select_related(
            "category",
            "poster",
            "poster__rank",
            "poster__ban_cache",
            "poster__online_tracker",
        ).filter(is_event=True)

        if first_post:
            queryset = queryset.filter(pk__gt=first_post.pk)
        if last_post:
            queryset = queryset.filter(pk__lt=last_post.pk)

        queryset = exclude_invisible_posts(request.user_acl, thread.category, queryset)
        return list(queryset.order_by("-id")[:limit])

    def get_frontend_context(self):
        context = {
            "results": PostSerializer(
                self.posts, many=True, context={"user": self._user}
            ).data
        }

        context.update(self.paginator)

        return context

    def get_template_context(self):
        return {"posts": self.posts, "paginator": self.paginator}


class ThreadPosts(ViewModel):
    pass
