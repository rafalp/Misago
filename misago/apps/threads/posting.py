from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.forumbase.mixins import RedirectToPostMixin
from misago.apps.forumbase.posting import NewThreadBaseView
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
        # Set flash and redirect user to his post
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("New thread has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(NewThreadBaseView, TypeMixin):
    pass


class NewReplyView(NewThreadBaseView, TypeMixin):
    pass

class EditReplyView(NewThreadBaseView, TypeMixin):
    pass