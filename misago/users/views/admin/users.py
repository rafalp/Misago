from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from misago.admin.auth import start_admin_session
from misago.admin.views import generic
from misago.conf import settings
from misago.core.mail import mail_users

from misago.users.forms.admin import (StaffFlagUserFormFactory, NewUserForm,
                                      EditUserForm, SearchUsersForm)
from misago.users.models import ACTIVATION_REQUIRED_NONE, User
from misago.users.signatures import set_user_signature


class UserAdmin(generic.AdminBaseMixin):
    root_link = 'misago:admin:users:accounts:index'
    templates_dir = 'misago/admin/users'

    def get_model(self):
        return get_user_model()

    def create_form_type(self, request, target):
        if request.user.is_superuser:
            add_staff_field = request.user.pk != target.id
        else:
            add_staff_field = False

        return StaffFlagUserFormFactory(
            self.Form, target, add_staff_field=add_staff_field)


class UsersList(UserAdmin, generic.ListView):
    items_per_page = 20
    ordering = (
        ('-id', _("From newest")),
        ('id', _("From oldest")),
        ('username_slug', _("A to z")),
        ('-username_slug', _("Z to a")),
    )
    selection_label = _('With users: 0')
    empty_selection_label = _('Select users')
    mass_actions = [
        {
            'action': 'activate',
            'name': _("Activate accounts"),
            'icon': 'fa fa-check',
        }
    ]

    def get_queryset(self):
        qs = super(UsersList, self).get_queryset()
        return qs.select_related('rank')

    def get_search_form(self, request):
        return SearchUsersForm

    def action_activate(self, request, users):
        inactive_users = []
        for user in users:
            if user.requires_activation:
                inactive_users.append(user)

        if not inactive_users:
            message = _("You have to select inactive users.")
            raise generic.MassActionError(message)
        else:
            activated_users_pks = [u.pk for u in inactive_users]
            queryset = User.objects.filter(pk__in=activated_users_pks)
            queryset.update(requires_activation=ACTIVATION_REQUIRED_NONE)

            mail_subject = _("Your account on %(forum_title)s "
                             "forums has been activated")
            subject_formats = {'forum_title': settings.forum_name}
            mail_subject = mail_subject % subject_formats

            mail_subject =  mail_subject
            mail_users(request, inactive_users, mail_subject,
                       'misago/emails/activation/by_admin')

            message = _("Selected users accounts have been activated.")
            messages.success(request, message)


class NewUser(UserAdmin, generic.ModelFormView):
    Form = NewUserForm
    template = 'new.html'
    message_submit = _('New user "%s" has been registered.')

    def handle_form(self, form, request, target):
        User = get_user_model()
        new_user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['new_password'],
            title=form.cleaned_data['title'],
            rank=form.cleaned_data.get('rank'),
            joined_from_ip=request._misago_real_ip)

        if form.cleaned_data.get('staff_level'):
            new_user.staff_level = form.cleaned_data['staff_level']

        if form.cleaned_data.get('roles'):
            new_user.roles.add(*form.cleaned_data['roles'])

        new_user.update_acl_key()
        new_user.save()

        messages.success(request, self.message_submit % target.username)
        return redirect('misago:admin:users:accounts:edit',
                        user_id=new_user.pk)


class EditUser(UserAdmin, generic.ModelFormView):
    Form = EditUserForm
    template = 'edit.html'
    message_submit = _('User "%s" has been edited.')

    def real_dispatch(self, request, target):
        target.old_username = target.username
        return super(EditUser, self).real_dispatch(request, target)

    def handle_form(self, form, request, target):
        target.username = target.old_username
        target.set_username(form.cleaned_data.get('username'))

        if form.cleaned_data.get('new_password'):
            target.set_password(form.cleaned_data['new_password'])

            if target.pk == request.user.pk:
                start_admin_session(request, target)
                update_session_auth_hash(request, target)

        if form.cleaned_data.get('email'):
            target.set_email(form.cleaned_data['email'])

        if form.cleaned_data.get('staff_level'):
            form.instance.staff_level = form.cleaned_data['staff_level']

        if form.cleaned_data.get('roles'):
            form.instance.roles.add(*form.cleaned_data['roles'])

        set_user_signature(target, form.cleaned_data.get('signature'))

        form.instance.update_acl_key()
        form.instance.save()

        messages.success(request, self.message_submit % target.username)
