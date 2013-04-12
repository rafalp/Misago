from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.messages import Message
from misago.models import Forum, Thread, Post, Checkpoint
from misago.apps.threadtype.base import ViewBase

class DeleteHideBaseView(ViewBase):
    def set_context(self):
        pass

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

        if self.kwargs.get('checkpoint'):
            self.checkpoint = self.post.checkpoint_set.get(id=self.kwargs.get('checkpoint'))
            self.request.acl.threads.allow_checkpoint_view(self.forum, self.checkpoint)

        self.set_context()

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.parents = []
        try:
            self._type_available()
            self._set_context()
            self._check_permissions()
            self.delete()
            self.message()
            return self.response()
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist, Checkpoint.DoesNotExist):
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))


class DeleteThreadBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_delete_thread(self.request.user, self.proxy,
                                                     self.thread, self.thread.start_post, True)

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


class ShowThreadBaseView(DeleteHideBaseView):
    def set_context(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_threads']:
            raise ACLError403(_("You cannot undelete this thread."))
        if not self.thread.start_post.deleted:
            raise ACLError403(_('This thread is already visible!'))

    def delete(self):
        self.thread.start_post.deleted = False
        self.thread.start_post.save(force_update=True)
        self.thread.last_post.set_checkpoint(self.request, 'undeleted')
        self.thread.last_post.save(force_update=True)
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_('Thread "%(thread)s" has been restored.') % {'thread': self.thread.name}), 'success', 'threads')

    def response(self):
        if self.request.acl.threads.can_see_deleted_threads(self.thread.forum):
            return redirect(reverse(self.type_prefix, kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))
        return self.threads_list_redirect()


class DeleteReplyBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_delete_post(self.request.user, self.forum,
                                                   self.thread, self.post, True)

    def delete(self):
        self.post.delete()
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_("Selected reply has been deleted.")), 'success', 'threads')

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
        self.request.messages.set_flash(Message(_("Selected reply has been deleted.")), 'success', 'threads_%s' % self.post.pk)

    def response(self):
        return self.redirect_to_post(self.post)


class ShowReplyBaseView(DeleteHideBaseView):
    def set_context(self):
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_posts']:
            raise ACLError403(_("You cannot undelete this reply."))
        if not self.post.deleted:
            raise ACLError403(_('This reply is already visible!'))

    def delete(self):
        self.post.deleted = False
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
        self.request.messages.set_flash(Message(_("Selected reply has been restored.")), 'success', 'threads_%s' % self.post.pk)

    def response(self):
        return self.redirect_to_post(self.post)


class DeleteCheckpointBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_checkpoint_delete(self.forum)

    def delete(self):
        self.checkpoint.delete()
        self.post.checkpoints = self.post.checkpoint_set.count() > 0
        self.post.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_("Selected checkpoint has been deleted.")), 'success', 'threads_%s' % self.post.pk)

    def response(self):
        return self.redirect_to_post(self.post)


class HideCheckpointBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_checkpoint_hide(self.forum)
        if self.checkpoint.deleted:
            raise ACLError403(_('This checkpoint is already hidden!'))

    def delete(self):
        self.checkpoint.deleted = True
        self.checkpoint.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_("Selected checkpoint has been hidden.")), 'success', 'threads_%s' % self.post.pk)

    def response(self):
        return self.redirect_to_post(self.post)


class ShowCheckpointBaseView(DeleteHideBaseView):
    def set_context(self):
        self.request.acl.threads.allow_checkpoint_show(self.forum)
        if not self.checkpoint.deleted:
            raise ACLError403(_('This checkpoint is already visible!'))

    def delete(self):
        self.checkpoint.deleted = False
        self.checkpoint.save(force_update=True)

    def message(self):
        self.request.messages.set_flash(Message(_("Selected checkpoint has been restored.")), 'success', 'threads_%s' % self.post.pk)

    def response(self):
        return self.redirect_to_post(self.post)