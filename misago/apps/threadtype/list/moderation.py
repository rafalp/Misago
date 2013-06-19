from django.forms import ValidationError
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.forms import FormLayout
from misago.messages import Message
from misago.models import Forum, Thread, Post
from misago.apps.threadtype.list.forms import MoveThreadsForm, MergeThreadsForm
from misago.utils.strings import slugify

class ThreadsListModeration(object):
    def action_accept(self, ids):
        if self._action_accept(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been marked as reviewed and made visible to other members.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were marked as reviewed.')), 'info', 'threads')

    def _action_accept(self, ids):
        accepted = 0
        users = []
        for thread in self.threads:
            if thread.pk in ids and thread.moderated:
                accepted += 1
                # Sync thread and post
                thread.moderated = False
                thread.replies_moderated -= 1
                thread.save(force_update=True)
                thread.start_post.moderated = False
                thread.start_post.save(force_update=True)
                thread.set_checkpoint(self.request, 'accepted')
                # Sync user
                if thread.last_post.user:
                    thread.start_post.user.threads += 1
                    thread.start_post.user.posts += 1
                    users.append(thread.start_post.user)
        if accepted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) + accepted
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + accepted
            self.forum.sync()
            self.forum.save(force_update=True)
            for user in users:
                user.save(force_update=True)
        return accepted

    def action_annouce(self, ids):
        if self._action_annouce(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been turned into announcements.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were turned into announcements.')), 'info', 'threads')

    def _action_annouce(self, ids):
        acl = self.request.acl.threads.get_role(self.forum)
        annouced = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight < 2:
                annouced.append(thread.pk)
        if annouced:
            Thread.objects.filter(id__in=annouced).update(weight=2)
        return annouced

    def action_sticky(self, ids):
        if self._action_sticky(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been sticked to the top of list.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were turned into stickies.')), 'info', 'threads')

    def _action_sticky(self, ids):
        acl = self.request.acl.threads.get_role(self.forum)
        sticky = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight != 1 and (acl['can_pin_threads'] == 2 or thread.weight < 2):
                sticky.append(thread.pk)
        if sticky:
            Thread.objects.filter(id__in=sticky).update(weight=1)
        return sticky

    def action_normal(self, ids):
        if self._action_normal(ids):
            self.request.messages.set_flash(Message(_('Selected threads weight has been removed.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads have had their weight removed.')), 'info', 'threads')

    def _action_normal(self, ids):
        normalised = []
        for thread in self.threads:
            if thread.pk in ids and thread.weight > 0:
                normalised.append(thread.pk)
        if normalised:
            Thread.objects.filter(id__in=normalised).update(weight=0)
        return normalised

    def action_move(self, ids):
        threads = []
        for thread in self.threads:
            if thread.pk in ids:
                threads.append(thread)
        if self.request.POST.get('origin') == 'move_form':
            form = MoveThreadsForm(self.request.POST, request=self.request, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                for thread in threads:
                    thread.move_to(new_forum)
                    thread.save(force_update=True)
                    thread.set_checkpoint(self.request, 'moved', forum=self.forum)
                new_forum.sync()
                new_forum.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                self.request.messages.set_flash(Message(_('Selected threads have been moved to "%(forum)s".') % {'forum': new_forum.name}), 'success', 'threads')
                return None
            self.message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MoveThreadsForm(request=self.request, forum=self.forum)
        return self.request.theme.render_to_response('%ss/move_threads.html' % self.type_prefix,
                                                     {
                                                      'type_prefix': self.type_prefix,
                                                      'message': self.message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'threads': threads,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def action_merge(self, ids):
        if len(ids) < 2:
            raise ValidationError(_("You have to pick two or more threads to merge."))
        threads = []
        for thread in self.threads:
            if thread.pk in ids:
                threads.append(thread)
        if self.request.POST.get('origin') == 'merge_form':
            form = MergeThreadsForm(self.request.POST, request=self.request, threads=threads)
            if form.is_valid():
                new_thread = Thread.objects.create(
                                                   forum=form.cleaned_data['new_forum'],
                                                   name=form.cleaned_data['thread_name'],
                                                   slug=slugify(form.cleaned_data['thread_name']),
                                                   start=timezone.now(),
                                                   last=timezone.now()
                                                   )
                merged = []
                for thread in reversed(threads):
                    merged.append(thread.pk)
                    thread.merge_with(new_thread)
                Thread.objects.filter(id__in=merged).delete()
                new_thread.sync()
                new_thread.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                if form.cleaned_data['new_forum'].pk != self.forum.pk:
                    form.cleaned_data['new_forum'].sync()
                    form.cleaned_data['new_forum'].save(force_update=True)
                self.request.messages.set_flash(Message(_('Selected threads have been merged into new one.')), 'success', 'threads')
                return None
            self.message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MergeThreadsForm(request=self.request, threads=threads)

        warning = None
        lookback = threads[0].last_post_id
        for thread in threads[1:]:
            if thread.start_post_id < lookback:
                warning = Message(_("Warning: Posting times in one or more threads overlaps. This may result in disturbed flow of merged thread."), 'warning')
                break
            else:
                lookback = thread.last_post_id

        return self.request.theme.render_to_response(('%ss/merge.html' % self.type_prefix),
                                                     {
                                                      'type_prefix': self.type_prefix,
                                                      'message': self.message,
                                                      'warning': warning,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'threads': threads,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def action_open(self, ids):
        if self._action_open(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been opened.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were opened.')), 'info', 'threads')

    def _action_open(self, ids):        
        opened = []
        for thread in self.threads:
            if thread.pk in ids and thread.closed:
                opened.append(thread.pk)
                thread.set_checkpoint(self.request, 'opened')
        if opened:
            Thread.objects.filter(id__in=opened).update(closed=False)
        return opened

    def action_close(self, ids):
        if self._action_close(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been closed.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were closed.')), 'info', 'threads')

    def _action_close(self, ids):
        closed = []
        for thread in self.threads:
            if thread.pk in ids and not thread.closed:
                closed.append(thread.pk)
                thread.set_checkpoint(self.request, 'closed')
        if closed:
            Thread.objects.filter(id__in=closed).update(closed=True)
        return closed

    def action_undelete(self, ids):
        if self._action_undelete(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been restored.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were restored.')), 'info', 'threads')

    def _action_undelete(self, ids):
        undeleted = []
        posts = 0
        for thread in self.threads:
            if thread.pk in ids and thread.deleted:
                undeleted.append(thread.pk)
                posts += thread.replies + 1
                thread.start_post.deleted = False
                thread.start_post.save(force_update=True)
                thread.set_checkpoint(self.request, 'undeleted')
        if undeleted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) + len(undeleted)
            self.request.monitor['posts'] = int(self.request.monitor['posts']) + posts
            self.forum.sync()
            self.forum.save(force_update=True)
            Thread.objects.filter(id__in=undeleted).update(deleted=False)
        return undeleted

    def action_soft(self, ids):
        if self._action_soft(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been hidden.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were hidden.')), 'info', 'threads')

    def _action_soft(self, ids):
        deleted = []
        posts = 0
        for thread in self.threads:
            if thread.pk in ids and not thread.deleted:
                deleted.append(thread.pk)
                posts += thread.replies + 1
                thread.start_post.deleted = True
                thread.start_post.save(force_update=True)
                thread.set_checkpoint(self.request, 'deleted')
        if deleted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) - len(deleted)
            self.request.monitor['posts'] = int(self.request.monitor['posts']) - posts
            self.forum.sync()
            self.forum.save(force_update=True)
            Thread.objects.filter(id__in=deleted).update(deleted=True)
        return deleted

    def action_hard(self, ids):
        if self._action_hard(ids):
            self.request.messages.set_flash(Message(_('Selected threads have been deleted.')), 'success', 'threads')
        else:
            self.request.messages.set_flash(Message(_('No threads were deleted.')), 'info', 'threads')
    
    def _action_hard(self, ids):        
        deleted = []
        posts = 0
        for thread in self.threads:
            if thread.pk in ids:
                deleted.append(thread.pk)
                posts += thread.replies + 1
                thread.delete()
        if deleted:
            self.request.monitor['threads'] = int(self.request.monitor['threads']) - len(deleted)
            self.request.monitor['posts'] = int(self.request.monitor['posts']) - posts
            self.forum.sync()
            self.forum.save(force_update=True)
        return deleted
