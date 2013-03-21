from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.announcements.forms import NewThreadForm, EditThreadForm
from misago.apps.announcements.mixins import TypeMixin

class NewThreadView(NewThreadBaseView, TypeMixin):
    action = 'new_thread'
    form_type = NewThreadForm

    def set_forum_context(self):
        self.forum = Forum.objects.get(special='announcements')

    def response(self):
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("New announcement has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_("New announcement has been posted.")), 'success', 'threads')
        return redirect(reverse('announcement', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(EditThreadBaseView, TypeMixin):
    action = 'edit_thread'
    form_type = EditThreadForm
    
    def response(self):
        self.request.messages.set_flash(Message(_("Announcement has been edited.")), 'success', 'threads_%s' % self.post.pk)
        return redirect(reverse('announcement', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))
