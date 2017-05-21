from math import ceil

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views import View

from misago.conf import settings
from misago.threads.permissions import exclude_invisible_posts
from misago.threads.viewmodels import ForumThread, PrivateThread


class GotoView(View):
    thread = None
    read_aware = False

    def get(self, request, pk, slug, **kwargs):
        thread = self.get_thread(request, pk, slug).unwrap()
        self.test_permissions(request, thread)

        posts_queryset = exclude_invisible_posts(request.user, thread.category, thread.post_set)

        target_post = self.get_target_post(thread, posts_queryset.order_by('id'), **kwargs)
        target_page = self.compute_post_page(target_post, posts_queryset)

        return self.get_redirect(thread, target_post, target_page)

    def get_thread(self, request, pk, slug):
        return self.thread(request, pk, slug, read_aware=self.read_aware)

    def test_permissions(self, request, thread):
        pass

    def get_target_post(self, thread, posts_queryset):
        raise NotImplementedError("goto views should define their own get_target_post method")

    def compute_post_page(self, target_post, posts_queryset):
        # filter out events
        posts_queryset = posts_queryset.filter(is_event=False)

        thread_len = posts_queryset.count()
        if thread_len <= settings.MISAGO_POSTS_PER_PAGE + settings.MISAGO_POSTS_TAIL:
            return 1  # no chance for post to be on other page than only page

        # compute total count of thread pages
        hits = max(1, thread_len - settings.MISAGO_POSTS_TAIL)
        hits += int(ceil(hits / float(settings.MISAGO_POSTS_PER_PAGE)))
        thread_pages = int(ceil(hits / float(settings.MISAGO_POSTS_PER_PAGE)))

        # is target an event?
        if target_post.is_event:
            target_event = target_post
            previous_posts = posts_queryset.filter(pk__lt=target_event.pk)
            target_post = previous_posts.order_by('id').last()

        # resolve post's page
        post_offset = posts_queryset.filter(pk__lte=target_post.pk).count()
        hits = max(1, post_offset)
        hits += int(ceil(hits / float(settings.MISAGO_POSTS_PER_PAGE)))
        post_page = int(ceil(hits / float(settings.MISAGO_POSTS_PER_PAGE)))

        if post_page > thread_pages:
            post_page = thread_pages

        return post_page

    def get_redirect(self, thread, target_post, target_page):
        thread_url = thread.thread_type.get_thread_absolute_url(thread, target_page)
        return redirect('%s#post-%s' % (thread_url, target_post.pk))


class ThreadGotoPostView(GotoView):
    thread = ForumThread

    def get_target_post(self, thread, posts_queryset, **kwargs):
        return get_object_or_404(posts_queryset, pk=kwargs['post'])


class ThreadGotoLastView(GotoView):
    thread = ForumThread

    def get_target_post(self, thread, posts_queryset, **kwargs):
        return posts_queryset.order_by('id').last()


class ThreadGotoNewView(GotoView):
    thread = ForumThread
    read_aware = True

    def get_target_post(self, thread, posts_queryset, **kwargs):
        if thread.is_new:
            return posts_queryset.filter(
                posted_on__gt=thread.last_read_on,
            ).order_by('id').first()
        else:
            return posts_queryset.order_by('id').last()


class ThreadGotoUnapprovedView(GotoView):
    thread = ForumThread

    def test_permissions(self, request, thread):
        if not thread.acl['can_approve']:
            raise PermissionDenied(
                _(
                    "You need permission to approve content to "
                    "be able to go to first unapproved post."
                )
            )

    def get_target_post(self, thread, posts_queryset, **kwargs):
        unapproved_post = posts_queryset.filter(
            is_unapproved=True,
        ).order_by('id').first()
        if unapproved_post:
            return unapproved_post
        else:
            return posts_queryset.order_by('id').last()


class PrivateThreadGotoPostView(GotoView):
    thread = PrivateThread

    def get_target_post(self, thread, posts_queryset, **kwargs):
        return get_object_or_404(posts_queryset, pk=kwargs['post'])


class PrivateThreadGotoLastView(GotoView):
    thread = PrivateThread

    def get_target_post(self, thread, posts_queryset, **kwargs):
        return posts_queryset.order_by('id').last()


class PrivateThreadGotoNewView(GotoView):
    thread = PrivateThread
    read_aware = True

    def get_target_post(self, thread, posts_queryset, **kwargs):
        if thread.is_new:
            return posts_queryset.filter(
                posted_on__gt=thread.last_read_on,
            ).order_by('id').first()
        else:
            return posts_queryset.order_by('id').last()
