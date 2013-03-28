from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.privatethreads.forms import (NewThreadForm, EditThreadForm,
                                              NewReplyForm, EditReplyForm)
from misago.apps.privatethreads.mixins import TypeMixin

class NewThreadView(NewThreadBaseView, TypeMixin):
    form_type = NewThreadForm

    def set_forum_context(self):
        self.forum = Forum.objects.get(special='private_threads')

    def after_form(self, form):
        self.thread.participants.add(self.request.user)
        self.invite_users(form.invite_users)
        self.whitelist_mentions()
        self.force_stats_sync()

    def response(self):
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("New thread has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
        return redirect(reverse('private_thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(EditThreadBaseView, TypeMixin):
    form_type = EditThreadForm

    def after_form(self, form):
        self.whitelist_mentions()
    
    def response(self):
        self.request.messages.set_flash(Message(_("Your thread has been edited.")), 'success', 'threads_%s' % self.post.pk)
        return redirect(reverse('private_thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(NewReplyBaseView, TypeMixin):
    form_type = NewReplyForm

    def after_form(self, form):
        try:
            self.invite_users(form.invite_users)
        except AttributeError:
            pass
        self.whitelist_mentions()
        self.force_stats_sync()

    def response(self):
        if self.post.moderated:
            self.request.messages.set_flash(Message(_("Your reply has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads_%s' % self.post.pk)
        else:
            self.request.messages.set_flash(Message(_("Your reply has been posted.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(EditReplyBaseView, TypeMixin):
    form_type = EditReplyForm

    def after_form(self, form):
        self.whitelist_mentions()

    def response(self):
        self.request.messages.set_flash(Message(_("Your reply has been changed.")), 'success', 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)