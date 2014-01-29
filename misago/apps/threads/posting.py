from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403
from misago.apps.threads.forms import NewThreadForm, EditThreadForm
from misago.apps.threadtype.posting import NewThreadBaseView, EditThreadBaseView, NewReplyBaseView, EditReplyBaseView
from misago.models import Forum, Thread, Post, Poll, PollOption, WarnLevel
from misago.apps.threads.mixins import TypeMixin


class PollFormMixin(object):
    def create_poll(self, form):
        poll = Poll(forum=self.forum,
                    thread=self.thread,
                    user=self.request.user,
                    user_name=self.request.user.username,
                    user_slug=self.request.user.username_slug,
                    start_date=timezone.now(),
                    length=form.cleaned_data['poll_length'],
                    question=form.cleaned_data['poll_question'],
                    max_choices=form.cleaned_data['poll_max_choices'],
                    vote_changing=form.cleaned_data['poll_changing_votes'],
                    public=form.cleaned_data['poll_max_choices'])
        poll.save()

        choices = []
        for name in form.clean_choices:
            option = PollOption.objects.create(
                                               poll=poll,
                                               forum=self.forum,
                                               thread=self.thread,
                                               name=name,
                                               )
            choices.append(option)

        poll.choices_cache = choices
        poll.save()

        self.thread.has_poll = True
        self.thread.save()

    def update_poll(self, form):
        poll = self.thread.poll
        poll.question = form.cleaned_data['poll_question']
        poll.max_choices = form.cleaned_data['poll_max_choices']
        poll.length = form.cleaned_data['poll_length']
        poll.vote_changing = form.cleaned_data['poll_changing_votes']
        self.update_poll_choices(poll, form)
        poll.save()

    def update_poll_choices(self, poll, form):
        for option in form.changed_choices:
            option.save(force_update=True)
        for option in form.deleted_choices:
            poll.votes -= option.votes
            option.delete()
        for name in form.new_choices:
            option = PollOption.objects.create(
                                               poll=poll,
                                               forum=self.forum,
                                               thread=self.thread,
                                               name=name,
                                               )
        poll.choices_cache = [x for x in poll.option_set.all()]

    def delete_poll(self):
        self.thread.poll.delete()


class PrefixFormMixin(object):
    def set_prefix(self, form):
        if form.cleaned_data['thread_prefix']:
            self.thread.prefix_id = form.cleaned_data['thread_prefix']
        else:
            self.thread.prefix = None
        self.thread.save()


class NewThreadView(NewThreadBaseView, TypeMixin, PollFormMixin, PrefixFormMixin):
    form_type = NewThreadForm

    def set_forum_context(self):
        self.forum = Forum.objects.get(pk=self.kwargs.get('forum'), type='forum')

    def check_permissions(self):
        if self.request.user.warning_level_disallows_writing_threads:
            raise ACLError403(_("You can't start new threads due to your warning level."))

    def force_moderation(self):
        return self.request.user.warning_level_moderate_new_threads

    def after_form(self, form):
        if form.cleaned_data.get('poll_question'):
            self.create_poll(form)

        if form.cleaned_data.get('thread_prefix') != None:
            self.set_prefix(form)

    def response(self):
        if self.post.moderated:
            messages.success(self.request, _("New thread has been posted. It will be hidden from other members until moderator reviews it."), 'threads')
        else:
            messages.success(self.request, _("New thread has been posted."), 'threads')
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class EditThreadView(EditThreadBaseView, TypeMixin, PollFormMixin, PrefixFormMixin):
    form_type = EditThreadForm

    def after_form(self, form):
        if self.thread.poll and self.request.acl.threads.can_edit_poll(self.forum, self.thread.poll):
            if form.cleaned_data.get('poll_delete'):
                self.delete_poll()
                self.thread.save()
            else:
                self.update_poll(form)
        elif form.cleaned_data.get('poll_question'):
            self.create_poll(form)

        if form.cleaned_data.get('thread_prefix') != None:
            self.set_prefix(form)

    def response(self):
        messages.success(self.request, _("Your thread has been edited."), 'threads_%s' % self.post.pk)
        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % self.post.pk))


class NewReplyView(NewReplyBaseView, TypeMixin):
    def check_permissions(self):
        if self.request.user.warning_level_disallows_writing_replies:
            raise ACLError403(_("You can't reply to threads due to your warning level."))

    def force_moderation(self):
        return self.request.user.warning_level_moderate_new_replies

    def response(self):
        if self.post.moderated:
            messages.success(self.request, _("Your reply has been posted. It will be hidden from other members until moderator reviews it."), 'threads_%s' % self.post.pk)
        else:
            messages.success(self.request, _("Your reply has been posted."), 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)


class EditReplyView(EditReplyBaseView, TypeMixin):
    def response(self):
        messages.success(self.request, _("Your reply has been changed."), 'threads_%s' % self.post.pk)
        return self.redirect_to_post(self.post)
