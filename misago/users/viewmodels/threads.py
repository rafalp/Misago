from misago.acl import add_acl
from misago.conf import settings
from misago.core.shortcuts import paginate, pagination_dict
from misago.threads.permissions import exclude_invisible_threads
from misago.threads.serializers import FeedSerializer
from misago.threads.utils import add_categories_to_items
from misago.threads.viewmodels import ThreadsRootCategory


class UserThreads(object):
    def __init__(self, request, profile, page=0):
        root_category = ThreadsRootCategory(request)
        threads_categories = [root_category.unwrap()] + root_category.subcategories

        threads_queryset = self.get_threads_queryset(request, threads_categories, profile)

        posts_queryset = self.get_posts_queryset(request.user, profile, threads_queryset).filter(
            is_event=False,
            is_hidden=False,
            is_unapproved=False,
        ).order_by('-id')

        list_page = paginate(
            posts_queryset, page, settings.MISAGO_POSTS_PER_PAGE, settings.MISAGO_POSTS_TAIL
        )
        paginator = pagination_dict(list_page)

        posts = list(list_page.object_list)
        threads = []

        for post in posts:
            threads.append(post.thread)

        add_categories_to_items(root_category.unwrap(), threads_categories, posts + threads)

        add_acl(request.user, threads)
        add_acl(request.user, posts)

        self._user = request.user

        self.posts = posts
        self.paginator = paginator

    def get_threads_queryset(self, request, threads_categories, profile):
        return exclude_invisible_threads(request.user, threads_categories, profile.thread_set)

    def get_posts_queryset(self, user, profile, threads_queryset):
        return profile.post_set.select_related('thread', 'poster').filter(
            id__in=threads_queryset.values('first_post_id'),
        )

    def get_frontend_context(self):
        context = {
            'results': UserFeedSerializer(self.posts, many=True, context={'user': self._user}).data
        }

        context.update(self.paginator)

        return context

    def get_template_context(self):
        return {
            'posts': self.posts,
            'paginator': self.paginator,
        }


UserFeedSerializer = FeedSerializer.exclude_fields('poster')
