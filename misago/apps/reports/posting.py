from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.posting import EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.reports.mixins import TypeMixin
from misago.apps.reports.forms import EditThreadForm, NewReplyForm, EditReplyForm

class SetStateCheckpointMixin(object):
    def post_form(self, form):
        self.thread.original_weight = self.thread_weight
        super(SetStateCheckpointMixin, self).post_form(form)
        if self.thread.original_weight != self.thread_weight:
            if self.thread.original_weight == 2:
                self.request.monitor.decrease('reported_posts')
            if self.thread.weight == 1:
                self.thread.set_checkpoint(self.request, 'resolved')
            if self.thread.weight == 0:
                self.thread.set_checkpoint(self.request, 'bogus')


class EditThreadView(SetStateCheckpointMixin, EditThreadBaseView, TypeMixin):
    form_type = EditThreadForm

    def response(self):
        self.request.messages.set_flash(Message(_("Report has been edited.")), 'success', 'threads_%s' % self.post.pk)
        return redirect(reverse('report', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(SetStateCheckpointMixin, NewReplyBaseView, TypeMixin):
    form_type = NewReplyForm

    def response(self):
        self.request.messages.set_flash(Message(_("Your reply has been posted.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(SetStateCheckpointMixin, EditReplyBaseView, TypeMixin):
    form_type = EditReplyForm
    
    def response(self):
        self.request.messages.set_flash(Message(_("Your reply has been changed.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)
