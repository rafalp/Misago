import warnings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from misago.acl import versions
from misago.admin.views import generic
from misago.forums.models import FORUMS_TREE_ID, Forum
from misago.forums.forms import ForumFormFactory, DeleteFormFactory


class ForumAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:forums:nodes:index'
    Model = Forum
    templates_dir = 'misago/admin/forums'
    message_404 = _("Requested forum does not exist.")

    def get_target(self, kwargs):
        target = super(ForumAdmin, self).get_target(kwargs)

        target_is_special = bool(target.special_role)
        target_not_in_forums_tree = target.tree_id != FORUMS_TREE_ID

        if target.pk and (target_is_special or target_not_in_forums_tree):
            raise Forum.DoesNotExist()
        else:
            return target


class ForumsList(ForumAdmin, generic.ListView):
    def get_queryset(self):
        return Forum.objects.all_forums()

    def process_context(self, request, context):
        context['items'] = [f for f in context['items']]

        children_lists = {}

        for i, item in enumerate(context['items']):
            item.level_range = range(item.level - 1)
            item.first = False
            item.last = False
            children_lists.setdefault(item.parent_id, []).append(item)

        for level_items in children_lists.values():
            level_items[0].first = True
            level_items[-1].last = True

        return context


class ForumFormMixin(object):
    def create_form_type(self, request, target):
        return ForumFormFactory(target)

    def handle_form(self, form, request, target):
        if form.instance.pk:
            if form.instance.parent_id != form.cleaned_data['new_parent'].pk:
                form.instance.move_to(form.cleaned_data['new_parent'],
                                      position='last-child')
            form.instance.save()
        else:
            form.instance.insert_at(form.cleaned_data['new_parent'],
                                    position='last-child',
                                    save=True)

        cachebuster.invalidate()
        messages.success(request, self.message_submit % target.name)


class NewForum(ForumFormMixin, ForumAdmin, generic.ModelFormView):
    message_submit = _('New forum "%s" has been saved.')


class EditForum(ForumFormMixin, ForumAdmin, generic.ModelFormView):
    message_submit = _('Forum "%s" has been edited.')


class DeleteForum(ForumAdmin, generic.ModelFormView):
    message_submit = _('Forum "%s" has been deleted.')
    template = 'delete.html'

    def create_form_type(self, request, target):
        return DeleteFormFactory(target)

    def handle_form(self, form, request, target):
        move_children_to = form.cleaned_data.get('move_children_to')
        if move_children_to:
            for child in target.get_children():
                Forum.objects.move_node(child, move_children_to, 'last-child')
        else:
            for child in target.get_descendants().order_by('-lft'):
                child.delete()

        move_threads_to = form.cleaned_data.get('move_threads_to')
        if move_threads_to:
            warnings.warn("Not implemented yet! See #354 for details.",
                          FutureWarning)

        form.instance.delete()
        cachebuster.invalidate()

        messages.success(request, self.message_submit % target.name)
        return redirect(self.root_link)


class MoveUpForum(ForumAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = target.get_previous_sibling()
        except Forum.DoesNotExist:
            other_target = None

        if other_target:
            Forum.objects.move_node(target, other_target, 'left')
            message = _('Forum "%s" has been moved up.') % target.name
            messages.success(request, message)


class MoveDownForum(ForumAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = target.get_next_sibling()
        except Forum.DoesNotExist:
            other_target = None

        if other_target:
            Forum.objects.move_node(target, other_target, 'right')
            message = _('Forum "%s" has been moved down.') % target.name
            messages.success(request, message)
