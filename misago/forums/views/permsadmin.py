from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic
from misago.acl import version as acl_version
from misago.acl.forms import get_permissions_forms
from misago.acl.models import Role
from misago.acl.views import RoleAdmin, RolesList

from misago.forums.forms import (ForumRoleForm, ForumRolesACLFormFactory,
                                 RoleForumACLFormFactory)
from misago.forums.views.forumsadmin import ForumAdmin, ForumsList
from misago.forums.models import Forum, ForumRole, RoleForumACL


class ForumRoleAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:permissions:forums:index'
    Model = ForumRole
    templates_dir = 'misago/admin/forumroles'
    message_404 = _("Requested role does not exist.")


class ForumRolesList(ForumRoleAdmin, generic.ListView):
    ordering = (('name', None),)


class RoleFormMixin(object):
    def real_dispatch(self, request, target):
        form = ForumRoleForm(instance=target)

        perms_forms = get_permissions_forms(target)

        if request.method == 'POST':
            perms_forms = get_permissions_forms(target, request.POST)
            valid_forms = 0
            for permissions_form in perms_forms:
                if permissions_form.is_valid():
                    valid_forms += 1

            form = ForumRoleForm(request.POST, instance=target)
            if form.is_valid() and len(perms_forms) == valid_forms:
                new_permissions = {}
                for permissions_form in perms_forms:
                    cleaned_data = permissions_form.cleaned_data
                    new_permissions[permissions_form.prefix] = cleaned_data

                form.instance.permissions = new_permissions
                form.instance.save()

                messages.success(request, self.message_submit % target.name)

                if 'stay' in request.POST:
                    return redirect(request.path)
                else:
                    return redirect(self.root_link)

        return self.render(
            request,
            {
                'form': form,
                'target': target,
                'perms_forms': perms_forms,
            })


class NewForumRole(RoleFormMixin, ForumRoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%s" has been saved.')


class EditForumRole(RoleFormMixin, ForumRoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%s" has been changed.')


class DeleteForumRole(ForumRoleAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.special_role:
            message = _('Role "%s" is special role and can\'t be deleted.')
            return message % target.name

    def button_action(self, request, target):
        target.delete()
        message = _('Role "%s" has been deleted.') % unicode(target.name)
        messages.success(request, message)


"""
Create forum roles view for assinging roles to forum,
add link to it in forums list
"""
class ForumPermissions(ForumAdmin, generic.ModelFormView):
    templates_dir = 'misago/admin/forumroles'
    template = 'forumroles.html'

    def real_dispatch(self, request, target):
        forum_roles = ForumRole.objects.order_by('name')

        assigned_roles = {}
        for acl in target.forum_role_set.select_related('forum_role'):
            assigned_roles[acl.role_id] = acl.forum_role

        forms = []
        forms_are_valid = True
        for role in Role.objects.order_by('name'):
            FormType = ForumRolesACLFormFactory(role,
                                                forum_roles,
                                                assigned_roles.get(role.pk))

            if request.method == 'POST':
                forms.append(FormType(request.POST, prefix=role.pk))
                if not forms[-1].is_valid():
                    forms_are_valid = False
            else:
                forms.append(FormType(prefix=role.pk))

        if request.method == 'POST' and forms_are_valid:
            target.forum_role_set.all().delete()
            new_permissions = []
            for form in forms:
                if form.cleaned_data['forum_role']:
                    new_permissions.append(
                        RoleForumACL(
                            role=form.role,
                            forum=target,
                            forum_role=form.cleaned_data['forum_role']
                        ))
            if new_permissions:
                RoleForumACL.objects.bulk_create(new_permissions)

            acl_version.invalidate()

            message = _("Forum %s permissions have been changed.")
            messages.success(request, message % target)
            if 'stay' in request.POST:
                return redirect(request.path)
            else:
                return redirect(self.root_link)

        return self.render(
            request,
            {
                'forms': forms,
                'target': target,
            })


ForumsList.add_item_action(
    name=_("Forum permissions"),
    icon='fa fa-adjust',
    link='misago:admin:forums:nodes:permissions',
    style='success')


"""
Create role forums view for assinging forums to role,
add link to it in user roles list
"""
class RoleForumsACL(RoleAdmin, generic.ModelFormView):
    templates_dir = 'misago/admin/forumroles'
    template = 'roleforums.html'

    def real_dispatch(self, request, target):
        forums = Forum.objects.all_forums()
        roles = ForumRole.objects.order_by('name')

        if not forums:
            messages.info(request, _("No forums exist."))
            return redirect(self.root_link)

        choices = {}
        for choice in target.forums_acls.select_related('forum_role'):
            choices[choice.forum_id] = choice.forum_role

        forms = []
        forms_are_valid = True
        for forum in forums:
            forum.level_range = range(forum.level - 1)
            FormType = RoleForumACLFormFactory(forum,
                                               roles,
                                               choices.get(forum.pk))

            if request.method == 'POST':
                forms.append(FormType(request.POST, prefix=forum.pk))
                if not forms[-1].is_valid():
                    forms_are_valid = False
            else:
                forms.append(FormType(prefix=forum.pk))

        if request.method == 'POST' and forms_are_valid:
            target.forums_acls.all().delete()
            new_permissions = []
            for form in forms:
                if form.cleaned_data['role']:
                    new_permissions.append(
                        RoleForumACL(role=target,
                                     forum=form.forum,
                                     forum_role=form.cleaned_data['role']))
            if new_permissions:
                RoleForumACL.objects.bulk_create(new_permissions)

            acl_version.invalidate()

            message = _("Forum permissions for role %s have been changed.")
            messages.success(request, message % target)
            if 'stay' in request.POST:
                return redirect(request.path)
            else:
                return redirect(self.root_link)

        return self.render(
            request,
            {
                'forms': forms,
                'target': target,
            })
RolesList.add_item_action(
    name=_("Forums permissions"),
    icon='fa fa-comments-o',
    link='misago:admin:permissions:users:forums',
    style='success')
