from ...threads.models import Thread
from .threads import UserThreads


class UserPosts(UserThreads):
    def get_threads_queryset(self, request, threads_categories, profile):
        return Thread.objects.filter(category__in=threads_categories)

    def get_posts_queryset(self, user, profile, threads_queryset):
        return profile.post_set.select_related("thread", "poster").filter(
            thread_id__in=threads_queryset.values("id")
        )
