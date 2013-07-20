from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.models import Forum, Thread, Post, User
from misago.apps.privatethreads.forms import (NewThreadForm, EditThreadForm,
                                              NewReplyForm, EditReplyForm)
from misago.apps.privatethreads.mixins import TypeMixin

class NewThreadView(NewThreadBaseView, TypeMixin):
    form_type = NewThreadForm

    def set_forum_context(self):
        self.forum = Forum.objects.get(special='private_threads')

    def form_initial_data(self):
        if self.kwargs.get('user'):
            try:
                user = User.objects.get(id=self.kwargs.get('user'))
                acl = user.acl(self.request)
                if not acl.private_threads.can_participate():
                    raise ACLError403(_("This member can not participate in private threads."))
                if (not self.request.acl.private_threads.can_invite_ignoring() and
                        not user.allow_pd_invite(self.request.user)):
                    raise ACLError403(_('%(user)s restricts who can invite him to private threads.') % {'user': user.username})
                return {'invite_users': user.username}
            except User.DoesNotExist:
                raise ACLError404()
        return {}

    def after_form(self, form):
        self.thread.participants.add(self.request.user)
        self.invite_users(form.invite_users)
        self.whitelist_mentions()
        self.force_stats_sync()

    def response(self):
        if self.post.moderated:
            messages.success(self.request, _("New thread has been posted. It will be hidden from other members until moderator reviews it."), 'threads')
        else:
            messages.success(self.request, _("New thread has been posted."), 'threads')
        return redirect(reverse('private_thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(EditThreadBaseView, TypeMixin):
    form_type = EditThreadForm

    def after_form(self, form):
        self.whitelist_mentions()

    def response(self):
        messages.success(self.request, _("Your thread has been edited."), 'threads_%s' % self.post.pk)
        return redirect(reverse('private_thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(NewReplyBaseView, TypeMixin):
    form_type = NewReplyForm

    def set_context(self):
        super(NewReplyView, self).set_context()
        if not (self.request.acl.private_threads.is_mod() or self.thread.participants.count() > 1):
            raise ACLError403(_("This thread needs to have more than one participant to allow new replies."))

    def after_form(self, form):
        try:
            self.invite_users(form.invite_users)
        except AttributeError:
            pass
        self.whitelist_mentions()
        self.force_stats_sync()

    def response(self):
        if self.post.moderated:
            messages.success(self.request, _("Your reply has been posted. It will be hidden from other members until moderator reviews it."), 'threads_%s' % self.post.pk)
        else:
            messages.success(self.request, _("Your reply has been posted."), 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(EditReplyBaseView, TypeMixin):
    form_type = EditReplyForm

    def after_form(self, form):
        self.whitelist_mentions()

    def response(self):
        messages.success(self.request, _("Your reply has been changed."), 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)