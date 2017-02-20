from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads

from .threads import UserThreads


class UserPosts(UserThreads):
    def get_threads_queryset(self, request, threads_categories, profile):
        return exclude_invisible_threads(request.user, threads_categories, Thread.objects)

    def get_posts_queryset(self, user, profile, threads_queryset):
        return profile.post_set.select_related('thread', 'poster').filter(
            thread_id__in=threads_queryset.values('id')
        )
