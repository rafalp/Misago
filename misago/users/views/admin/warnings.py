from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from misago.admin.views import generic

from misago.users.models import WarningLevel
from misago.users.forms.admin import WarningLevelForm


class WarningsAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:warnings:index'
    Model = WarningLevel
    Form = WarningLevelForm
    templates_dir = 'misago/admin/warnings'
    message_404 = _("Requested warning level does not exist.")


class WarningsList(WarningsAdmin, generic.ListView):
    ordering = (('level', None),)


class NewWarning(WarningsAdmin, generic.ModelFormView):
    message_submit = _('New warning level "%(name)s" has been saved.')


class EditWarning(WarningsAdmin, generic.ModelFormView):
    message_submit = _('Warning level "%(name)s" has been edited.')


class DeleteWarning(WarningsAdmin, generic.ButtonView):
    def button_action(self, request, target):
        target.delete()
        message = _('Warning level "%(name)s" has been deleted.')
        messages.success(request, message % {'name': target.name})


class MoveDownWarning(WarningsAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = WarningLevel.objects.filter(level__gt=target.level)
            other_target = other_target.earliest('level')
        except WarningLevel.DoesNotExist:
            other_target = None

        if other_target:
            other_target.level, target.level = target.level, other_target.level
            other_target.save(update_fields=['level'])
            target.save(update_fields=['level'])

            message = _('Warning level "%(name)s" has '
                        'been moved below "%(other)s".')
            targets_names = {'name': target.name, 'other': other_target.name}
            messages.success(request, message % targets_names)


class MoveUpWarning(WarningsAdmin, generic.ButtonView):
    def button_action(self, request, target):
        try:
            other_target = WarningLevel.objects.filter(level__lt=target.level)
            other_target = other_target.latest('level')
        except WarningLevel.DoesNotExist:
            other_target = None

        if other_target:
            other_target.level, target.level = target.level, other_target.level
            other_target.save(update_fields=['level'])
            target.save(update_fields=['level'])

            message = _('Warning level "%(name)s" has '
                        'been moved above "%(other)s".')
            targets_names = {'name': target.name, 'other': other_target.name}
            messages.success(request, message % targets_names)
