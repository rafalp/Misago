from django.utils.deprecation import MiddlewareMixin

from misago.categories.models import Category

from .models import Thread
from .viewmodels import filter_read_threads_queryset


class UnreadThreadsCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_anonymous:
            return

        if not request.user.acl_cache['can_use_private_threads']:
            return

        if not request.user.sync_unread_private_threads:
            return

        participated_threads = request.user.threadparticipant_set.values('thread_id')

        category = Category.objects.private_threads()
        threads = Thread.objects.filter(category=category, id__in=participated_threads)

        new_threads = filter_read_threads_queryset(request.user, [category], 'new', threads)
        unread_threads = filter_read_threads_queryset(request.user, [category], 'unread', threads)

        request.user.unread_private_threads = new_threads.count() + unread_threads.count()
        request.user.sync_unread_private_threads = False

        request.user.save(
            update_fields=[
                'unread_private_threads',
                'sync_unread_private_threads',
            ]
        )
