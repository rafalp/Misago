from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forums.models import Forum
from misago.messages import Message
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination

class DeleteView(BaseView):
    def fetch_thread(self, kwargs):
        self.thread = Thread.objects.get(pk=kwargs['thread'])
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        if self.mode in ['tread_delete', 'hide_thread']:
            self.request.acl.threads.allow_delete_thread(
                                                         self.request.user,
                                                         self.forum,
                                                         self.thread,
                                                         self.thread.start_post,
                                                         self.mode == 'delete_thread')
            # Assert we are not user trying to delete thread with replies
            acl = self.request.acl.threads.get_role(self.thread.forum_id)
            if not acl['can_delete_threads']:
                if self.thread.post_set.exclude(user_id=self.request.user.id).count() > 0:
                    raise ACLError403(_("Somebody has already replied to this thread. You cannot delete it."))
            
    def fetch_post(self, kwargs):
        self.post = self.thread.post_set.get(pk=kwargs['post'])
        if self.post.pk == self.thread.start_post_id:
            raise Post.DoesNotExist()
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)
        self.request.acl.threads.allow_delete_post(
                                                   self.request.user,
                                                   self.forum,
                                                   self.thread,
                                                   self.post,
                                                   self.mode == 'delete_post')
        acl = self.request.acl.threads.get_role(self.thread.forum_id)
        if not acl['can_delete_posts'] and self.thread.post_set.filter(id__gt=self.post.pk).count() > 0:
            raise ACLError403(_("Somebody has already replied to this post, you cannot delete it."))
        
    def __call__(self, request, **kwargs):
        self.request = request
        self.mode = kwargs['mode']
        try:
            if not request.user.is_authenticated():
                raise ACLError403(_("Guest, you have to sign-in in order to be able to delete replies."))
            self.fetch_thread(kwargs)
            if self.mode in ['hide_post', 'delete_post']:
                self.fetch_post(kwargs)
        except (Thread.DoesNotExist, Post.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        
        if self.mode == 'delete_thread':
            self.thread.delete()
            self.forum.sync()
            self.forum.save(force_update=True)
            request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')
            return redirect(reverse('forum', kwargs={'forum': self.thread.forum.pk, 'slug': self.thread.forum.slug}))
        
        if self.mode == 'hide_thread':
            self.thread.start_post.deleted = True
            self.thread.start_post.save(force_update=True)
            self.thread.last_post.set_checkpoint(request, 'deleted')
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')
            if request.acl.threads.can_see_deleted_threads(self.thread.forum):
                return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))
            return redirect(reverse('forum', kwargs={'forum': self.thread.forum.pk, 'slug': self.thread.forum.slug}))
        
        if self.mode == 'delete_post':
            self.post.delete()
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            request.messages.set_flash(Message(_("Selected Reply has been deleted.")), 'success', 'threads')
            return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}))
            
        if self.mode == 'hide_post':
            self.post.deleted = True
            self.post.edit_date = timezone.now()
            self.post.edit_user = request.user
            self.post.edit_user_name = request.user.username
            self.post.edit_user_slug = request.user.username_slug
            self.post.save(force_update=True)
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            request.messages.set_flash(Message(_("Selected Reply has been deleted.")), 'success', 'threads_%s' % self.post.pk)
            return self.redirect_to_post(self.post)