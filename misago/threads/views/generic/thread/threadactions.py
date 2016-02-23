from django.contrib import messages
from django.db.transaction import atomic
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.categories.lists import get_category_path

from misago.threads import moderation
from misago.threads.forms.moderation import MoveThreadForm
from misago.threads.models import Label
from misago.threads.views.generic.actions import ActionsBase


__all__ = ['ThreadActions']


class ThreadActions(ActionsBase):
    query_key = 'thread_action'
    is_mass_action = False

    def get_available_actions(self, kwargs):
        self.thread = kwargs['thread']
        self.category = self.thread.category

        actions = []

        if self.thread.acl['can_change_label']:
            self.category.labels = Label.objects.get_category_labels(self.category)
            for label in self.category.labels:
                if label.pk != self.thread.label_id:
                    name = _('Label as "%(label)s"') % {'label': label.name}
                    actions.append({
                        'action': 'label:%s' % label.slug,
                        'icon': 'tag',
                        'name': name
                    })

            if self.category.labels and self.thread.label_id:
                actions.append({
                    'action': 'unlabel',
                    'icon': 'times-circle',
                    'name': _("Remove label")
                })

        if self.thread.acl['can_pin']:
            if self.thread.is_pinned:
                actions.append({
                    'action': 'unpin',
                    'icon': 'circle',
                    'name': _("Unpin thread")
                })
            else:
                actions.append({
                    'action': 'pin',
                    'icon': 'star',
                    'name': _("Pin thread")
                })

        if self.thread.acl['can_review']:
            if self.thread.is_moderated:
                actions.append({
                    'action': 'approve',
                    'icon': 'check',
                    'name': _("Approve thread")
                })

        if self.thread.acl['can_move']:
            actions.append({
                'action': 'move',
                'icon': 'arrow-right',
                'name': _("Move thread")
            })

        if self.thread.acl['can_close']:
            if self.thread.is_closed:
                actions.append({
                    'action': 'open',
                    'icon': 'unlock-alt',
                    'name': _("Open thread")
                })
            else:
                actions.append({
                    'action': 'close',
                    'icon': 'lock',
                    'name': _("Close thread")
                })

        if self.thread.acl['can_hide']:
            if self.thread.is_hidden:
                actions.append({
                    'action': 'unhide',
                    'icon': 'eye',
                    'name': _("Reveal thread")
                })
            else:
                actions.append({
                    'action': 'hide',
                    'icon': 'eye-slash',
                    'name': _("Hide thread")
                })

        if self.thread.acl['can_hide'] == 2:
            actions.append({
                'action': 'delete',
                'icon': 'times',
                'name': _("Delete thread"),
                'confirmation': _("Are you sure you want to delete this "
                                  "thread? This action can't be undone.")
            })

        return actions

    def action_label(self, request, thread, label_slug):
        for label in self.category.labels:
            if label.slug == label_slug:
                break
        else:
            raise moderation.ModerationError(self.invalid_action_message)

        moderation.label_thread(request.user, thread, label)
        message = _('Thread was labeled "%(label)s".')
        messages.success(request, message % {'label': label.name})

    def action_unlabel(self, request, thread):
        moderation.unlabel_thread(request.user, thread)
        messages.success(request, _("Thread label was removed."))

    def action_pin(self, request, thread):
        moderation.pin_thread(request.user, thread)
        messages.success(request, _("Thread was pinned."))

    def action_unpin(self, request, thread):
        moderation.unpin_thread(request.user, thread)
        messages.success(request, _("Thread was unpinned."))

    def action_approve(self, request, thread):
        moderation.approve_thread(request.user, thread)
        messages.success(request, _("Thread was approved."))

    move_thread_full_template = 'misago/thread/move/full.html'
    move_thread_modal_template = 'misago/thread/move/modal.html'

    def action_move(self, request, thread):
        form = MoveThreadForm(acl=request.user.acl, category=self.category)

        if 'submit' in request.POST:
            form = MoveThreadForm(
                request.POST, acl=request.user.acl, category=self.category)
            if form.is_valid():
                new_category = form.cleaned_data['new_category']

                with atomic():
                    moderation.move_thread(request.user, thread, new_category)

                    self.category.lock()
                    new_category.lock()

                    self.category.synchronize()
                    self.category.save()
                    new_category.synchronize()
                    new_category.save()

                message = _('Thread was moved to "%(category)s".')
                messages.success(request, message % {
                    'category': new_category.name
                })

                return None # trigger thread refresh

        if request.is_ajax():
            template = self.move_thread_modal_template
        else:
            template = self.move_thread_full_template

        return render(request, template, {
            'form': form,
            'category': self.category,
            'path': get_category_path(self.category),
            'thread': thread
        })

    def action_close(self, request, thread):
        moderation.close_thread(request.user, thread)
        messages.success(request, _("Thread was closed."))

    def action_open(self, request, thread):
        moderation.open_thread(request.user, thread)
        messages.success(request, _("Thread was opened."))

    def action_unhide(self, request, thread):
        moderation.unhide_thread(request.user, thread)
        self.category.synchronize()
        self.category.save()
        messages.success(request, _("Thread was made visible."))

    def action_hide(self, request, thread):
        with atomic():
            self.category.lock()
            moderation.hide_thread(request.user, thread)
            self.category.synchronize()
            self.category.save()

        messages.success(request, _("Thread was hid."))

    def action_delete(self, request, thread):
        with atomic():
            self.category.lock()
            moderation.delete_thread(request.user, thread)
            self.category.synchronize()
            self.category.save()

        message = _('Thread "%(thread)s" was deleted.')
        messages.success(request, message % {'thread': thread.title})

        return redirect(self.category.get_absolute_url())
