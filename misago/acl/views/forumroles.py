from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.acl.models import ForumRole
from misago.acl.forms import ForumRoleForm


class ForumRoleAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:permissions:forums:index'
    Model = ForumRole
    Form = ForumRoleForm
    templates_dir = 'misago/admin/forumroles'
    message_404 = _("Requested role does not exist.")


class ForumRolesList(ForumRoleAdmin, generic.ListView):
    ordering = (('name', None),)


class NewForumRole(ForumRoleAdmin, generic.ModelFormView):
    message_submit = _('New role "%s" has been saved.')


class EditForumRole(ForumRoleAdmin, generic.ModelFormView):
    message_submit = _('Role "%s" has been changed.')


class DeleteForumRole(ForumRoleAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Role "%s" has been deleted.') % unicode(target.name)
        messages.success(request, message)
