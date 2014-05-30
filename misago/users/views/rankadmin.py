from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from misago.admin.views import generic
from misago.users.models import Rank
from misago.users.forms.admin import RankForm


class RankAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:ranks:index'
    Model = Rank
    Form = RankForm
    templates_dir = 'misago/admin/ranks'
    message_404 = _("Requested rank does not exist.")

    def update_roles(self, target, roles):
        target.roles.clear()
        if roles:
            target.roles.add(*roles)

    def handle_form(self, form, request, target):
        super(RankAdmin, self).handle_form(form, request, target)
        self.update_roles(target, form.cleaned_data['roles'])


class RanksList(RankAdmin, generic.ListView):
    ordering = (('order', None),)


class NewRank(RankAdmin, generic.ModelFormView):
    message_submit = _('New rank "%s" has been saved.')


class EditRank(RankAdmin, generic.ModelFormView):
    message_submit = _('Rank "%s" has been edited.')


class DeleteRank(RankAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_default:
            message = _('Rank "%s" is default rank and '
                        'can\'t be deleted.')
            return message % unicode(target.name)
        if target.user_set.exists():
            message = _('Rank "%s" is assigned to users and '
                        'can\'t be deleted.')
            return message % unicode(target.name)

    def button_action(self, request, target):
        target.delete()
        message = _('Rank "%s" has been deleted.') % unicode(target.name)
        messages.success(request, message)


class MoveUpRank(RankAdmin, generic.ButtonView):
    def button_action(self, request, target):
        other_target = target.prev()
        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=['order'])
            target.save(update_fields=['order'])
            message = _('Rank "%s" has been moved up.') % unicode(target.name)
            messages.success(request, message)


class MoveDownRank(RankAdmin, generic.ButtonView):
    def button_action(self, request, target):
        other_target = target.next()
        if other_target:
            other_target.order, target.order = target.order, other_target.order
            other_target.save(update_fields=['order'])
            target.save(update_fields=['order'])
            message = _('Rank "%s" has been moved down.') % unicode(target.name)
            messages.success(request, message)


class DefaultRank(RankAdmin, generic.ButtonView):
    def check_permissions(self, request, target):
        if target.is_default:
            return _('Rank "%s" is already default.') % unicode(target.name)

    def button_action(self, request, target):
        Rank.objects.make_rank_default(target)
        message = _('Rank "%s" has been made default.')
        messages.success(request, message % unicode(target.name))
