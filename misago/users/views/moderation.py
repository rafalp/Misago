from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.decorators import require_POST
from misago.core.shortcuts import get_object_or_404, validate_slug

from misago.users.forms.rename import ChangeUsernameForm
from misago.users.decorators import deny_guests
from misago.users.permissions.moderation import (allow_rename_user,
                                                 allow_ban_username,
                                                 allow_ban_email)
from misago.users.permissions.delete import allow_delete_user
from misago.users.sites import user_profile


def user_moderation_view(required_permission=None):
    def wrap(f):
        @deny_guests
        @transaction.atomic
        def decorator(request, *args, **kwargs):
            queryset = get_user_model().objects
            user_id = kwargs.pop('user_id')

            kwargs['user'] = get_object_or_404(queryset, id=user_id)
            validate_slug(kwargs['user'], kwargs.pop('user_slug'))
            add_acl(request.user, kwargs['user'])

            if required_permission:
                required_permission(request.user, kwargs['user'])

            return f(request, *args, **kwargs)
        return decorator
    return wrap


@user_moderation_view(allow_rename_user)
def rename(request, user):
    form = ChangeUsernameForm(user=user)
    if request.method == 'POST':
        old_username = user.username
        form = ChangeUsernameForm(request.POST, user=user)
        if form.is_valid():
            try:
                form.change_username(changed_by=request.user)
                message = _("%(old_username)s's username has been changed.")
                message = message % {'old_username': old_username}
                messages.success(request, message)

                return redirect(user_profile.get_default_link(),
                                **{'user_slug': user.slug, 'user_id': user.pk})
            except IntegrityError:
                message = _("Error changing username. Please try again.")
                messages.error(request, message)

    return render(request, 'misago/modusers/rename.html',
                  {'profile': user, 'form': form})


@user_moderation_view(allow_ban_username)
def ban_username(request, user):
    form = ChangeUsernameForm(user=user)
    if request.method == 'POST':
        old_username = user.username
        form = ChangeUsernameForm(request.POST, user=user)
        if form.is_valid():
            user.set_username(form.cleaned_data['new_username'],
                              changed_by=request.user)
            user.save(update_fields=['username', 'slug'])

            message = _("%(old_username)s's username has been changed.")
            messages.success(request, message % {'old_username': old_username})

            return redirect(user_profile.get_default_link(),
                            **{'user_slug': user.slug, 'user_id': user.pk})

    return render(request, 'misago/modusers/rename.html',
                  {'profile': user, 'form': form})


@user_moderation_view(allow_ban_email)
def ban_email(request, user):
    form = ChangeUsernameForm(user=user)
    if request.method == 'POST':
        old_username = user.username
        form = ChangeUsernameForm(request.POST, user=user)
        if form.is_valid():
            user.set_username(form.cleaned_data['new_username'],
                              changed_by=request.user)
            user.save(update_fields=['username', 'slug'])

            message = _("%(old_username)s's username has been changed.")
            messages.success(request, message % {'old_username': old_username})

            return redirect(user_profile.get_default_link(),
                            **{'user_slug': user.slug, 'user_id': user.pk})

    return render(request, 'misago/modusers/rename.html',
                  {'profile': user, 'form': form})


@require_POST
@user_moderation_view(allow_delete_user)
def delete(request, user):
    user.delete(delete_content=True)

    message = _("User %(username)s has been deleted.")
    messages.success(request, message % {'username': user.username})
    return redirect('misago:index')
