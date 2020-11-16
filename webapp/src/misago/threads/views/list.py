from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ...core.shortcuts import get_int_or_404
from ..viewmodels import (
    ForumThreads,
    PrivateThreads,
    PrivateThreadsCategory,
    ThreadsCategory,
    ThreadsRootCategory,
)


class ThreadsList(View):
    category = None
    threads = None

    template_name = None

    def get(self, request, list_type=None, **kwargs):
        start = get_int_or_404(request.GET.get("start", 0))

        category = self.get_category(request, **kwargs)
        threads = self.get_threads(request, category, list_type, start)

        frontend_context = self.get_frontend_context(request, category, threads)
        request.frontend_context.update(frontend_context)

        template_context = self.get_template_context(request, category, threads)
        return render(request, self.template_name, template_context)

    def get_category(self, request, **kwargs):
        return self.category(request, **kwargs)  # pylint: disable=not-callable

    def get_threads(self, request, category, list_type, start):
        return self.threads(  # pylint: disable=not-callable
            request, category, list_type, start
        )

    def get_frontend_context(self, request, category, threads):
        context = self.get_default_frontend_context()

        context.update(category.get_frontend_context())
        context.update(threads.get_frontend_context())

        return context

    def get_default_frontend_context(self):
        return {}

    def get_template_context(self, request, category, threads):
        context = self.get_default_template_context()

        context.update(category.get_template_context())
        context.update(threads.get_template_context())

        return context

    def get_default_template_context(self):
        return {}


class ForumThreadsList(ThreadsList):
    category = ThreadsRootCategory
    threads = ForumThreads

    template_name = "misago/threadslist/threads.html"

    def get_default_frontend_context(self):
        return {"MERGE_THREADS_API": reverse("misago:api:thread-merge")}


class CategoryThreadsList(ForumThreadsList):
    category = ThreadsCategory

    template_name = "misago/threadslist/category.html"

    def get_category(self, request, **kwargs):
        category = super().get_category(request, **kwargs)
        if not category.level:
            raise Http404()  # disallow root category access
        return category


class PrivateThreadsList(ThreadsList):
    category = PrivateThreadsCategory
    threads = PrivateThreads

    template_name = "misago/threadslist/private_threads.html"
