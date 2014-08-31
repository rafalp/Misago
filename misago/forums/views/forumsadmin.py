from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.acl import version as acl_version

from misago.forums.models import FORUMS_TREE_ID, Forum, RoleForumACL
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
            if form.instance.parent_id != form.cleaned_data['new_parent'].pk:
                Forum.objects.clear_cache()
        else:
            form.instance.insert_at(form.cleaned_data['new_parent'],
                                    position='last-child',
                                    save=True)
            Forum.objects.clear_cache()

        if form.cleaned_data.get('copy_permissions'):
            form.instance.forum_role_set.all().delete()
            copy_from = form.cleaned_data['copy_permissions']

            copied_acls = []
            for acl in copy_from.forum_role_set.all():
                copied_acls.append(RoleForumACL(
                    role_id=acl.role_id,
                    forum=form.instance,
                    forum_role_id=acl.forum_role_id))

            if copied_acls:
                RoleForumACL.objects.bulk_create(copied_acls)

            acl_version.invalidate()

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
        move_threads_to = form.cleaned_data.get('move_threads_to')

        if move_children_to:
            for child in target.get_children():
                Forum.objects.move_node(child, move_children_to, 'last-child')
                if move_threads_to and child.pk == move_threads_to.pk:
                    move_threads_to = child
        else:
            for child in target.get_descendants().order_by('-lft'):
                child.delete_content()
                child.delete()

        if move_threads_to:
            target.move_content(move_threads_to)
            move_threads_to.recount()
            move_threads_to.save()
        else:
            target.delete_content()

        form.instance.delete()

        messages.success(request, self.message_submit % target.name)
        return redirect(self.root_link)


class MoveDownForum(ForumAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = target.get_next_sibling()
        except Forum.DoesNotExist:
            other_target = None

        if other_target:
            Forum.objects.move_node(target, other_target, 'right')
            Forum.objects.clear_cache()

            message = _('Forum "%s" has been moved below "%s".')
            targets_names = (target.name, other_target.name)
            messages.success(request, message % targets_names)


class MoveUpForum(ForumAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = target.get_previous_sibling()
        except Forum.DoesNotExist:
            other_target = None

        if other_target:
            Forum.objects.move_node(target, other_target, 'left')
            Forum.objects.clear_cache()

            message = _('Forum "%s" has been moved above "%s".')
            targets_names = (target.name, other_target.name)
            messages.success(request, message % targets_names)
