from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import pgettext

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
from .validators import validate_thread_solution


class ThreadSolutionView(GenericThreadView):
    backend = thread_backend


class ThreadSolutionSelectView(ThreadSolutionView):
    def post(
        self, request: HttpRequest, slug: str, thread_id: int, post_id: int
    ) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        new_solution = self.get_thread_post(request, thread, post_id, for_content=True)
        if new_solution.id == thread.solution_id:
            return self.get_thread_post_redirect(request, new_solution)

        if thread.solution_id:
            check_change_thread_solution_permission(
                request.user_permissions, new_solution
            )
            success_message = pgettext("post solution select view", "Solution changed")
        else:
            check_select_thread_solution_permission(
                request.user_permissions, new_solution
            )
            success_message = pgettext("post solution select view", "Solution selected")

        try:
            validate_thread_solution(new_solution, request)
        except ValidationError as error:
            raise PermissionDenied(error.messages[0])

        select_thread_solution(thread, new_solution, request.user, request=request)

        messages.success(request, success_message)

        return self.get_thread_post_redirect(request, new_solution)


class ThreadSolutionClearView(ThreadSolutionView):
    def post(self, request: HttpRequest, slug: str, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        old_solution = None
        if thread.solution_id:
            old_solution = self.get_thread_post(
                request, thread, thread.solution_id, for_content=True
            )

        if thread.solution_id:
            check_clear_thread_solution_permission(request.user_permissions, thread)
            clear_thread_solution(thread, request=request)
            messages.success(
                request, pgettext("post solution clear view", "Solution cleared")
            )

        if request.POST.get("next") == "post" and old_solution:
            return self.get_thread_post_redirect(request, old_solution)

        return redirect(self.get_next_thread_url(request, thread))


class ThreadSolutionLockView(ThreadSolutionView):
    thread_select_related = ("category", "solution")

    def post(self, request: HttpRequest, slug: str, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        if thread.solution_id:
            thread.solution = self.get_thread_post(
                request, thread, thread.solution_id, for_content=True
            )

        if thread.solution_id and not thread.solution_is_locked:
            check_lock_thread_solution_permission(request.user_permissions, thread)
            lock_thread_solution(thread, request.user, request=request)
            messages.success(
                request, pgettext("post solution select view", "Solution locked")
            )

        if request.POST.get("next") == "post" and thread.solution:
            return self.get_thread_post_redirect(request, thread.solution)

        return redirect(self.get_next_thread_url(request, thread))


class ThreadSolutionUnlockView(ThreadSolutionView):
    thread_select_related = ("category", "solution")

    def post(self, request: HttpRequest, slug: str, thread_id: int) -> HttpResponse:
        thread = self.get_thread(request, thread_id)

        if thread.solution_id:
            thread.solution = self.get_thread_post(
                request, thread, thread.solution_id, for_content=True
            )

        if thread.solution_id and thread.solution_is_locked:
            check_unlock_thread_solution_permission(request.user_permissions, thread)
            unlock_thread_solution(thread, request.user, request=request)
            messages.success(
                request, pgettext("post solution select view", "Solution unlocked")
            )

        if request.POST.get("next") == "post" and thread.solution:
            return self.get_thread_post_redirect(request, thread.solution)

        return redirect(self.get_next_thread_url(request, thread))
