from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from misago.acl import add_acl
from misago.core.shortcuts import paginate, pagination_dict, validate_slug

from misago.threads.mixins.threadview import ThreadViewMixin
from misago.threads.mixins.typemixins import ThreadMixin, PrivateThreadMixin
from misago.threads.permissions.threads import exclude_invisible_posts


class BaseThread(View, ThreadViewMixin):
    def get(self, request, slug, pk, page=0, **kwargs):
        thread = self.get_thread(request, pk)
        validate_slug(thread, slug)

        base_posts_queryset = thread.post_set.select_related('poster').order_by('id')
        posts_queryset = exclude_invisible_posts(request.user, thread.category, base_posts_queryset)

        list_page = paginate(posts_queryset, page, settings.MISAGO_POSTS_PER_PAGE, settings.MISAGO_THREAD_TAIL)
        paginator = pagination_dict(list_page, include_page_range=False)

        posts = list(list_page.object_list)

        request.frontend_context.update(self.set_frontend_context(request, thread, posts, paginator))
        return render(request, self.template_name, self.get_context_data(request, thread, posts, paginator))

    def set_frontend_context(self, request, thread, posts, paginator):
        return {}

    def get_context_data(self, request, thread, posts, paginator):
        return {
            'category': thread.category,
            'thread': thread,
            'posts': posts,

            'count': paginator['count'],
            'paginator': paginator,

            'url_name': ':'.join(request.resolver_match.namespaces + [request.resolver_match.url_name])
        }


class Thread(BaseThread, ThreadMixin):
    template_name = 'misago/thread/thread.html'


class PrivateThread(BaseThread, PrivateThreadMixin):
    template_name = 'misago/thread/private_thread.html'
