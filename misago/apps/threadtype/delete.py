from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.threadtype.base import ViewBase

class DeleteHideBaseView(ViewBase):
    def _set_context(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk)
        self.check_forum_type()
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)

        if self.kwargs.get('post'):
            self.post = self.thread.post_set.get(id=self.kwargs.get('post'))
            self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)

        self.set_context()

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.parents = []
        try:
            self._set_context()
            self.delete()
            self.message()
            return self.response()
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist):
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))


class DeleteThreadBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_delete_thread(self.request.user, self.proxy,
                                                     self.thread, self.thread.start_post, True)
        # Assert we are not user trying to delete thread with replies
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_threads']:
            if self.thread.post_set.exclude(user_id=self.request.user.id).count() > 0:
                raise ACLError403(_("Somebody has already replied to this thread. You cannot delete it."))

    def delete(self):
        self.thread.delete()
        self.forum.sync()
        self.forum.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')

    def response(self):
        return self.threads_list_redirect()


class HideThreadBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_delete_thread(self.request.user, self.proxy,
                                                     self.thread, self.thread.start_post)
        # Assert we are not user trying to delete thread with replies
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_threads']:
            if self.thread.post_set.exclude(user_id=self.request.user.id).count() > 0:
                raise ACLError403(_("Somebody has already replied to this thread. You cannot delete it."))

    def delete(self):
        self.thread.start_post.deleted = True
        self.thread.start_post.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'deleted')
        self.thread.last_post.save(force_update=True)
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')

    def response(self):
        if self.request.acl.threads.can_see_deleted_threads(self.thread.forum):
            return redirect(reverse(self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))
        return self.threads_list_redirect()


class DeleteReplyBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_delete_post(self.request.user, self.forum,
                                                   self.thread, self.post, True)
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_posts'] and self.thread.post_set.filter(id__gt=self.post.pk).count() > 0:
            raise ACLError403(_("Somebody has already replied to this post, you cannot delete it."))

    def delete(self):
        self.post.delete()
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_("Selected Reply has been deleted.")), 'success', 'threads')

    def response(self):
        return redirect(reverse(self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))


class HideReplyBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_delete_post(self.request.user, self.forum,
                                                   self.thread, self.post)
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_posts'] and self.thread.post_set.filter(id__gt=self.post.pk).count() > 0:
            raise ACLError403(_("Somebody has already replied to this post, you cannot delete it."))

    def delete(self):
        self.post.deleted = True
        self.post.edit_date = timezone.now()
        self.post.edit_user = self.request.user
        self.post.edit_user_name = self.request.user.username
        self.post.edit_user_slug = self.request.user.username_slug
        self.post.save(force_update=True)
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_("Selected Reply has been deleted.")), 'success', 'threads_%s' % self.post.pk)

    def response(self):
        return self.redirect_to_post(self.post)
