from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.errorpages import not_allowed

from misago.threads import permissions, moderation, goto
from misago.threads.forms.report import ReportPostForm
from misago.threads.reports import user_has_reported_post, report_post
from misago.threads.views.generic.base import ViewBase


__all__ = [
    'QuotePostView',
    'ApprovePostView',
    'UnhidePostView',
    'HidePostView',
    'DeletePostView',
    'ReportPostView'
]


class PostView(ViewBase):
    is_atomic = True
    require_post = True

    def dispatch(self, request, *args, **kwargs):
        if self.require_post and request.method != "POST":
            return not_allowed(request)

        post = None
        response = None

        if self.is_atomic:
            with atomic():
                post = self.get_post(request, True, **kwargs)
                response = self.real_dispatch(request, post)
        else:
            post = self.get_post(request, **kwargs)
            response = self.real_dispatch(request, post)

        if response:
            return response
        else:
            return self.redirect_to_post(request.user, post)

    def real_dispatch(self, request, post):
        raise NotImplementedError(
            "post views have to override real_dispatch method")

    def redirect_to_post(self, user, post):
        posts_qs = self.exclude_invisible_posts(post.thread.post_set,
                                                user,
                                                post.category,
                                                post.thread)
        return redirect(goto.post(post.thread, posts_qs, post))


class QuotePostView(PostView):
    is_atomic = False
    require_post = False

    def real_dispatch(self, request, post):
        quote_tpl = u'[quote="%s, post:%s, topic:%s"]\n%s\n[/quote]'
        formats = (post.poster_name, post.pk, post.thread_id, post.original)
        return JsonResponse({
            'quote': quote_tpl % formats
        })


class ApprovePostView(PostView):
    def real_dispatch(self, request, post):
        if not post.acl['can_approve']:
            raise PermissionDenied(_("You can't approve this post."))

        if post.id == post.thread.first_post_id:
            moderation.approve_thread(request.user, post.thread)
            messages.success(request, _("Thread has been approved."))
        else:
            moderation.approve_post(request.user, post)
            messages.success(request, _("Post has been approved."))

        post.thread.synchronize()
        post.thread.save()
        post.category.synchronize()
        post.category.save()


class UnhidePostView(PostView):
    is_atomic = False

    def real_dispatch(self, request, post):
        permissions.allow_unhide_post(request.user, post)
        moderation.unhide_post(request.user, post)
        messages.success(request, _("Post has been made visible."))


class HidePostView(PostView):
    is_atomic = False

    def real_dispatch(self, request, post):
        permissions.allow_hide_post(request.user, post)
        moderation.hide_post(request.user, post)
        messages.success(request, _("Post has been hidden."))


class DeletePostView(PostView):
    def real_dispatch(self, request, post):
        post_id = post.id

        permissions.allow_delete_post(request.user, post)
        moderation.delete_post(request.user, post)

        post.thread.synchronize()
        post.thread.save()
        post.category.synchronize()
        post.category.save()

        posts_qs = self.exclude_invisible_posts(post.thread.post_set,
                                                request.user,
                                                post.category,
                                                post.thread)
        posts_qs = posts_qs.select_related('thread', 'category')

        if post_id < post.thread.last_post_id:
            target_post = posts_qs.order_by('id').filter(id__gt=post_id)
        else:
            target_post = posts_qs.order_by('-id').filter(id__lt=post_id)

        target_post = target_post[:1][0]
        target_post.thread.category = target_post.category

        add_acl(request.user, target_post.category)
        add_acl(request.user, target_post.thread)
        add_acl(request.user, target_post)

        messages.success(request, _("Post has been deleted."))
        return self.redirect_to_post(request.user, target_post)


class ReportPostView(PostView):
    require_post = False

    template = 'misago/thread/report_modal.html'
    alerts_template = 'misago/thread/post_alerts.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return not_allowed(request)

        return super(ReportPostView, self).dispatch(request, *args, **kwargs)

    def real_dispatch(self, request, post):
        if not post.acl['can_report']:
            raise PermissionDenied(_("You can't report posts."))

        if user_has_reported_post(request.user, post):
            return JsonResponse({
                'is_reported': True,
                'message': _("You have already reported this post.")})

        form = ReportPostForm()
        if request.method == 'POST':
            form = ReportPostForm(request.POST)
            if form.is_valid():
                report_post(request,
                            post,
                            form.cleaned_data['report_message'])

                message = _("%(user)s's post has been "
                            "reported to moderators.")
                message = message % {'user': post.poster_name}
                return JsonResponse({
                    'message': message,
                    'label': _("Reported"),
                    'alerts': self.render_alerts(request, post)
                })
            else:
                field_errors = form.errors.get('report_message')
                if field_errors:
                    field_error = field_errors[0]
                else:
                    field_error = _("Error reporting post.")

                return JsonResponse({'is_error': True, 'message': field_error})

        return self.render(request, {'form': form})

    def render_alerts(self, request, post):
        return render(request, self.alerts_template, {
            'category': post.category,
            'thread': post.thread,
            'post': post
        }).content


