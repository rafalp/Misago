from django.core.paginator import EmptyPage, InvalidPage
from django.http import Http404

from ...acl.objectacl import add_acl_to_obj
from ...core.cursorpagination import get_page
from ...core.shortcuts import paginate, pagination_dict
from ...threads.permissions import exclude_invisible_threads
from ...threads.serializers import FeedSerializer
from ...threads.utils import add_categories_to_items
from ...threads.viewmodels import ThreadsRootCategory


class UserThreads:
    def __init__(self, request, profile, start=0):
        root_category = ThreadsRootCategory(request)
        threads_categories = [root_category.unwrap()] + root_category.subcategories

        threads_queryset = self.get_threads_queryset(
            request, threads_categories, profile
        )

        posts_queryset = (
            self.get_posts_queryset(request.user, profile, threads_queryset)
            .filter(is_event=False, is_hidden=False, is_unapproved=False)
            .order_by("-id")
        )

        try:
            list_page = get_page(
                posts_queryset, "-id", request.settings.posts_per_page, start
            )
        except (EmptyPage, InvalidPage):
            raise Http404()

        posts = list(list_page.object_list)
        threads = []

        for post in posts:
            threads.append(post.thread)

        add_categories_to_items(
            root_category.unwrap(), threads_categories, posts + threads
        )

        add_acl_to_obj(request.user_acl, threads)
        add_acl_to_obj(request.user_acl, posts)

        self._user = request.user

        self.posts = posts
        self.list_page = list_page

    def get_threads_queryset(self, request, threads_categories, profile):
        return exclude_invisible_threads(
            request.user_acl, threads_categories, profile.thread_set
        )

    def get_posts_queryset(self, user, profile, threads_queryset):
        return profile.post_set.select_related("thread", "poster").filter(
            id__in=threads_queryset.values("first_post_id")
        )

    def get_frontend_context(self):
        return {
            "results": UserFeedSerializer(
                self.posts, many=True, context={"user": self._user}
            ).data,
            "next": self.list_page.next,
        }

    def get_template_context(self):
        return {"posts": self.posts, "next": self.list_page.next}


UserFeedSerializer = FeedSerializer.exclude_fields("poster")
