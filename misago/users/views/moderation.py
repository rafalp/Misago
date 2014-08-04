from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.core.decorators import require_POST
from misago.core.shortcuts import get_object_or_404, validate_slug
from misago.markup import Editor

from misago.users import avatars
from misago.users.bans import get_user_ban
from misago.users.decorators import deny_guests
from misago.users.forms.rename import ChangeUsernameForm
from misago.users.forms.modusers import (BanForm, ModerateAvatarForm,
                                         ModerateSignatureForm)
from misago.users.models import Ban
from misago.users.permissions.moderation import (allow_rename_user,
                                                 allow_moderate_avatar,
                                                 allow_moderate_signature,
                                                 allow_ban_user,
                                                 allow_lift_ban)
from misago.users.permissions.delete import allow_delete_user
from misago.users.signatures import set_user_signature
from misago.users.sites import user_profile


def user_moderation_view(required_permission=None):
    def wrap(f):
        @deny_guests
        @transaction.atomic
        def decorator(request, *args, **kwargs):
            queryset = get_user_model().objects.select_for_update()
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
                form.change_username(changed_by=user)
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


@user_moderation_view(allow_moderate_avatar)
def moderate_avatar(request, user):
    form = ModerateAvatarForm(instance=user)

    return render(request, 'misago/modusers/avatar.html',
                  {'profile': user, 'form': form})


@user_moderation_view(allow_moderate_signature)
def moderate_signature(request, user):
    form = ModerateSignatureForm(instance=user)

    if request.method == 'POST':
        form = ModerateSignatureForm(request.POST, instance=user)
        if form.is_valid():
            changed_fields = (
                'signature',
                'signature_parsed',
                'signature_checksum',
                'is_signature_banned',
                'signature_ban_user_message',
                'signature_ban_staff_message'
            )

            set_user_signature(user, form.cleaned_data['signature'])
            user.save(update_fields=changed_fields)

            message = _("%(username)s's signature has been moderated.")
            message = message % {'username': user.username}
            messages.success(request, message)

            if 'stay' not in request.POST:
                return redirect(user_profile.get_default_link(),
                                **{'user_slug': user.slug, 'user_id': user.pk})

    acl = user.acl
    editor = Editor(form['signature'],
                    allow_blocks=acl['allow_signature_blocks'],
                    allow_links=acl['allow_signature_links'],
                    allow_images=acl['allow_signature_images'])

    return render(request, 'misago/modusers/signature.html',
                  {'profile': user, 'form': form, 'editor': editor})


@user_moderation_view(allow_ban_user)
def ban_user(request, user):
    form = BanForm(user=user)
    if request.method == 'POST':
        form = BanForm(request.POST, user=user)
        if form.is_valid():
            form.ban_user()

            message = _("%(username)s has been banned.")
            messages.success(request, message % {'username': user.username})

            return redirect(user_profile.get_default_link(),
                            **{'user_slug': user.slug, 'user_id': user.pk})

    return render(request, 'misago/modusers/ban.html',
                  {'profile': user, 'form': form})


@require_POST
@user_moderation_view(allow_lift_ban)
def lift_user_ban(request, user):
    user_ban = get_user_ban(user).ban
    user_ban.lift()
    user_ban.save()

    Ban.objects.invalidate_cache()

    message = _("%(username)s's ban has been lifted.")
    messages.success(request, message % {'username': user.username})

    return redirect(user_profile.get_default_link(),
                    **{'user_slug': user.slug, 'user_id': user.pk})



@require_POST
@user_moderation_view(allow_delete_user)
def delete(request, user):
    user.delete(delete_content=True)

    message = _("User %(username)s has been deleted.")
    messages.success(request, message % {'username': user.username})
    return redirect('misago:index')
