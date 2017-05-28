from django.shortcuts import render
from django.urls import reverse
from django.views import View

from misago.threads.viewmodels import ForumThread, PrivateThread, ThreadPosts


class ThreadBase(View):
    thread = None
    posts = ThreadPosts

    template_name = None

    def get(self, request, pk, slug, page=0):
        thread = self.get_thread(request, pk, slug)
        posts = self.get_posts(request, thread, page)

        frontend_context = self.get_frontend_context(request, thread, posts)
        request.frontend_context.update(frontend_context)

        template_context = self.get_template_context(request, thread, posts)
        return render(request, self.template_name, template_context)

    def get_thread(self, request, pk, slug):
        return self.thread(
            request, pk, slug, read_aware=True, subscription_aware=True, poll_votes_aware=True
        )

    def get_posts(self, request, thread, page):
        return self.posts(request, thread, page)

    def get_default_frontend_context(self):
        return {}

    def get_frontend_context(self, request, thread, posts):
        context = self.get_default_frontend_context()

        context.update({
            'THREAD': thread.get_frontend_context(),
            'POSTS': posts.get_frontend_context(),
        })

        return context

    def get_template_context(self, request, thread, posts):
        context = {
            'url_name': ':'.join(request.resolver_match.namespaces + [
                request.resolver_match.url_name,
            ])
        }

        context.update(thread.get_template_context())
        context.update(posts.get_template_context())

        return context


class ThreadView(ThreadBase):
    thread = ForumThread
    template_name = 'misago/thread/thread.html'

    def get_default_frontend_context(self):
        return {
            'THREADS_API': reverse('misago:api:thread-list'),
        }


class PrivateThreadView(ThreadBase):
    thread = PrivateThread
    template_name = 'misago/thread/private_thread.html'
