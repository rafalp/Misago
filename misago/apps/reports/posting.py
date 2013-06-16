from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.reports.mixins import TypeMixin

class EditThreadView(EditThreadBaseView, TypeMixin):
    def response(self):
        self.request.messages.set_flash(Message(_("Report has been edited.")), 'success', 'threads_%s' % self.post.pk)
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(NewReplyBaseView, TypeMixin):
    def response(self):
        self.request.messages.set_flash(Message(_("Your reply has been posted.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(EditReplyBaseView, TypeMixin):
    def response(self):
        self.request.messages.set_flash(Message(_("Your reply has been changed.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)
