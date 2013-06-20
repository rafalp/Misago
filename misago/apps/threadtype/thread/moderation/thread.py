from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forms import Form, FormLayout
from misago.messages import Message
from misago.apps.threadtype.list.forms import MoveThreadsForm

class ThreadModeration(object):
    def thread_action_accept(self):
        # Sync thread and post
        self.thread.moderated = False
        self.thread.replies_moderated -= 1
        self.thread.save(force_update=True)
        self.thread.start_post.moderated = False
        self.thread.start_post.save(force_update=True)
        self.thread.set_checkpoint(self.request, 'accepted')
        # Sync user
        if self.thread.last_post.user:
            self.thread.start_post.user.threads += 1
            self.thread.start_post.user.posts += 1
            self.thread.start_post.user.save(force_update=True)
        # Sync forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor.increase('threads')
        self.request.monitor.increase('posts', self.thread.replies + 1)
        # After
        self.after_thread_action_accept()

    def after_thread_action_accept(self):
        self.request.messages.set_flash(Message(_('Thread has been marked as reviewed and made visible to other members.')), 'success', 'threads')

    def thread_action_annouce(self):
        self.thread.weight = 2
        self.thread.save(force_update=True)
        self.after_thread_action_annouce()

    def after_thread_action_annouce(self):
        self.request.messages.set_flash(Message(_('Thread has been turned into announcement.')), 'success', 'threads')

    def thread_action_sticky(self):
        self.thread.weight = 1
        self.thread.save(force_update=True)
        self.after_thread_action_sticky()
    
    def after_thread_action_sticky(self):
        self.request.messages.set_flash(Message(_('Thread has been turned into sticky.')), 'success', 'threads')

    def thread_action_normal(self):
        self.thread.weight = 0
        self.thread.save(force_update=True)
        self.after_thread_action_normal()

    def after_thread_action_normal(self):
        self.request.messages.set_flash(Message(_('Thread weight has been changed to normal.')), 'success', 'threads')

    def thread_action_move(self):
        message = None
        if self.request.POST.get('do') == 'move':
            form = MoveThreadsForm(self.request.POST, request=self.request, forum=self.forum)
            if form.is_valid():
                new_forum = form.cleaned_data['new_forum']
                self.thread.move_to(new_forum)
                self.thread.save(force_update=True)
                self.thread.set_checkpoint(self.request, 'moved', forum=self.forum)
                self.forum.sync()
                self.forum.save(force_update=True)
                new_forum.sync()
                new_forum.save(force_update=True)
                self.request.messages.set_flash(Message(_('Thread has been moved to "%(forum)s".') % {'forum': new_forum.name}), 'success', 'threads')
                return None
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = MoveThreadsForm(request=self.request, forum=self.forum)
        return self.request.theme.render_to_response('%ss/move_thread.html' % self.type_prefix,
                                                     {
                                                      'type_prefix': self.type_prefix,
                                                      'message': message,
                                                      'forum': self.forum,
                                                      'parents': self.parents,
                                                      'thread': self.thread,
                                                      'form': FormLayout(form),
                                                      },
                                                     context_instance=RequestContext(self.request));

    def thread_action_open(self):
        self.thread.closed = False
        self.thread.save(force_update=True)
        self.thread.set_checkpoint(self.request, 'opened')
        self.after_thread_action_open()

    def after_thread_action_open(self):
        self.request.messages.set_flash(Message(_('Thread has been opened.')), 'success', 'threads')

    def thread_action_close(self):
        self.thread.closed = True
        self.thread.save(force_update=True)
        self.thread.set_checkpoint(self.request, 'closed')
        self.after_thread_action_close()

    def after_thread_action_close(self):
        self.request.messages.set_flash(Message(_('Thread has been closed.')), 'success', 'threads')

    def thread_action_undelete(self):
        # Update first post in thread
        self.thread.start_post.deleted = False
        self.thread.start_post.save(force_update=True)
        # Update thread
        self.thread.sync()
        self.thread.save(force_update=True)
        # Set checkpoint
        self.thread.set_checkpoint(self.request, 'undeleted')
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor.increase('threads')
        self.request.monitor.increase('posts', self.thread.replies + 1)
        self.after_thread_action_undelete()

    def after_thread_action_undelete(self):
        self.request.messages.set_flash(Message(_('Thread has been restored.')), 'success', 'threads')

    def thread_action_soft(self):
        # Update first post in thread
        self.thread.start_post.deleted = True
        self.thread.start_post.save(force_update=True)
        # Update thread
        self.thread.sync()
        self.thread.save(force_update=True)
        # Set checkpoint
        self.thread.set_checkpoint(self.request, 'deleted')
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor.decrease('threads')
        self.request.monitor.decrease('posts', self.thread.replies + 1)
        self.after_thread_action_soft()

    def after_thread_action_soft(self):
        self.request.messages.set_flash(Message(_('Thread has been hidden.')), 'success', 'threads')

    def thread_action_hard(self):
        # Delete thread
        self.thread.delete()
        # Update forum
        self.forum.sync()
        self.forum.save(force_update=True)
        # Update monitor
        self.request.monitor.decrease('threads')
        self.request.monitor.decrease('posts', self.thread.replies + 1)
        self.after_thread_action_hard()
        return self.threads_list_redirect()

    def after_thread_action_hard(self):
        self.request.messages.set_flash(Message(_('Thread "%(thread)s" has been deleted.') % {'thread': self.thread.name}), 'success', 'threads')
