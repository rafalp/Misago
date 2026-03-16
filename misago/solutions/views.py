from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from ..permissions.solutions import (
    check_change_thread_solution_permission,
    check_clear_thread_solution_permission,
    check_lock_thread_solution_permission,
    check_select_thread_solution_permission,
    check_unlock_thread_solution_permission,
)
from ..threads.views.backend import thread_backend
from ..threads.views.generic import GenericThreadView
from .solutions import (
    clear_thread_solution,
    lock_thread_solution,
    select_thread_solution,
    unlock_thread_solution,
)


class GenericThreadSolutionView(GenericThreadView):
    backend = thread_backend


class ThreadSolutionSelectView(GenericThreadSolutionView):
    def post(
        self, request: HttpRequest, slug: str, thread_id: int, post_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)
        new_solution = self.get_thread_post(request, thread, post_id, for_content=True)
        old_solution = None

        if thread.solution_id:
            old_solution = self.get_thread_post(
                request, thread, thread.solution_id, for_content=True
            )
            check_change_thread_solution_permission(
                request.user_permissions, new_solution
            )
        else:
            check_select_thread_solution_permission(
                request.user_permissions, new_solution
            )

        select_thread_solution(thread, new_solution, request.user, request=request)

        return self.get_thread_post_redirect(request, new_solution)


class ThreadSolutionClearView(GenericThreadSolutionView):
    def post(self, request: HttpRequest, slug: str, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        old_solution = None
        if thread.solution_id:
            old_solution = self.get_thread_post(
                request, thread, thread.solution_id, for_content=True
            )

        if old_solution:
            check_clear_thread_solution_permission(request.user_permissions, thread)
            clear_thread_solution(thread, request=request)

        if request.POST.get("next") == "post" and old_solution:
            return self.get_thread_post_redirect(request, old_solution)

        return redirect(self.get_next_thread_url(request, thread))


class ThreadSolutionLockView(GenericThreadSolutionView):
    thread_select_related = ("category", "solution")

    def post(self, request: HttpRequest, slug: str, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        if thread.solution_id and not thread.solution_is_locked:
            check_lock_thread_solution_permission(request.user_permissions, thread)
            lock_thread_solution(thread, request.user, request=request)

        return redirect(self.get_next_thread_url(request, thread))


class ThreadSolutionUnlockView(GenericThreadSolutionView):
    thread_select_related = ("category", "solution")

    def post(self, request: HttpRequest, slug: str, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        if thread.solution_id and thread.solution_is_locked:
            check_unlock_thread_solution_permission(request.user_permissions, thread)
            unlock_thread_solution(thread, request.user, request=request)

        return redirect(self.get_next_thread_url(request, thread))
