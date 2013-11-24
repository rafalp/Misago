from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago import messages
from misago.apps.threadtype.posting import EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.models import Forum, Thread, Post
from misago.monitor import monitor, UpdatingMonitor
from misago.apps.reports.mixins import TypeMixin
from misago.apps.reports.forms import EditThreadForm, NewReplyForm, EditReplyForm

class SetStateCheckpointMixin(object):
    def post_form(self, form):
        self.thread.original_weight = self.thread.weight
        super(SetStateCheckpointMixin, self).post_form(form)
        if self.thread.original_weight != self.thread.weight:
            if self.thread.original_weight == 2:
                with UpdatingMonitor() as cm:
                    monitor.decrease('reported_posts')
            if self.thread.weight == 1:
                self.thread.set_checkpoint(self.request, 'resolved')
            if self.thread.weight == 0:
                self.thread.set_checkpoint(self.request, 'bogus')


class EditThreadView(SetStateCheckpointMixin, EditThreadBaseView, TypeMixin):
    form_type = EditThreadForm

    def response(self):
        messages.success(self.request, _("Report has been edited."), 'threads_%s' % self.post.pk)
        return redirect(reverse('report', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(SetStateCheckpointMixin, NewReplyBaseView, TypeMixin):
    form_type = NewReplyForm

    def response(self):
        messages.success(self.request, _("Your reply has been posted."), 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(SetStateCheckpointMixin, EditReplyBaseView, TypeMixin):
    form_type = EditReplyForm

    def response(self):
        messages.success(self.request, _("Your reply has been changed."), 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)
