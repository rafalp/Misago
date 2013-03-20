from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.mixins import RedirectToPostMixin
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.threads.mixins import TypeMixin

class NewThreadView(NewThreadBaseView, TypeMixin):
    action = 'new_thread'

    def set_context(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')
        self.request.acl.forums.allow_forum_view(self.forum)
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.threads.allow_new_threads(self.proxy)

    def response(self):
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("New thread has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(EditThreadBaseView, TypeMixin):
    action = 'edit_thread'

    def set_context(self):
        self.thread = Thread.objects.get(pk=self.kwargs.get('thread'))
        self.forum = self.thread.forum
        self.proxy = Forum.objects.parents_aware_forum(self.forum)
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        self.post = self.thread.start_post
        self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.post)
        self.request.acl.threads.allow_thread_edit(self.request.user, self.proxy, self.thread, self.post)
    
    def response(self):
        self.request.messages.set_flash(Message(_("Your thread has been edited.")), 'success', 'threads_%s' % self.post.pk)
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(NewReplyBaseView, RedirectToPostMixin, TypeMixin):
    action = 'new_reply'

    def set_context(self):
        pass
        
    def response(self):
        if self.post.moderated:
            request.messages.set_flash(Message(_("Your reply has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads_%s' % self.post.pk)
        else:
            request.messages.set_flash(Message(_("Your reply has been posted.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(post)


class EditReplyView(EditReplyBaseView, RedirectToPostMixin, TypeMixin):
    pass