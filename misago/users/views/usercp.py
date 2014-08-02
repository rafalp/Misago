from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render as django_render
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.conf import settings
from misago.core.decorators import ajax_only, require_POST
from misago.core.exceptions import AjaxError
from misago.core.mail import mail_user
from misago.markup import Editor

from misago.users import avatars
from misago.users.decorators import deny_guests
from misago.users.forms.rename import ChangeUsernameForm
from misago.users.forms.usercp import (ChangeForumOptionsForm,
                                       EditSignatureForm,
                                       ChangeEmailPasswordForm)
from misago.users.signatures import set_user_signature
from misago.users.sites import usercp
from misago.users.changedcredentials import (cache_new_credentials,
                                             get_new_credentials)
from misago.users.namechanges import UsernameChanges


def render(request, template, context=None):
    context = context or {}
    context['pages'] = usercp.get_pages(request)

    for page in context['pages']:
        if page['is_active']:
            context['active_page'] = page
            break

    return django_render(request, template, context)


@deny_guests
def change_forum_options(request):
    form = ChangeForumOptionsForm(instance=request.user)
    if request.method == 'POST':
        form = ChangeForumOptionsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            message = _("Your forum options have been changed.")
            messages.success(request, message)

            return redirect('misago:usercp_change_forum_options')

    return render(request, 'misago/usercp/change_forum_options.html',
                  {'form': form})


@deny_guests
def change_avatar(request):
    avatar_size = max(settings.MISAGO_AVATARS_SIZES)

    if not request.user.is_avatar_banned and request.method == 'POST':
        if 'dl-gravatar' in request.POST and settings.allow_custom_avatars:
            try:
                avatars.gravatar.set_avatar(request.user)
                message = _("Gravatar was downloaded and set as new avatar.")
                messages.success(request, message)
            except avatars.gravatar.GravatarError:
                message = _("Failed to connect to Gravatar servers.")
                messages.info(request, message)
            except avatars.gravatar.NoGravatarAvailable:
                message = _("No Gravatar is associated "
                            "with your e-mail address.")
                messages.info(request, message)
        elif 'set-dynamic' in request.POST:
            avatars.dynamic.set_avatar(request.user)
            message = _("New avatar based on your account was set.")
            messages.success(request, message)
        return redirect('misago:usercp_change_avatar')

    return render(request, 'misago/usercp/change_avatar.html', {
        'avatar_size': avatar_size,
        'galleries_exist': avatars.gallery.galleries_exist(),
        'has_source_image': avatars.uploaded.has_original_avatar(request.user)
    })


def avatar_not_banned(f):
    def decorator(request, *args, **kwargs):
        if request.user.is_avatar_banned:
            message = _("You don't have permission to change your avatar.")
            messages.info(request, message)
            return redirect('misago:usercp_change_avatar')
        else:
            return f(request, *args, **kwargs)
    return decorator


@deny_guests
@avatar_not_banned
def upload_avatar(request):
    if not settings.allow_custom_avatars:
        messages.info(request, _("Avatar uploads are currently disabled."))
        return redirect('misago:usercp_change_avatar')

    return render(request, 'misago/usercp/upload_avatar.html', {
        'upload_limit': settings.avatar_upload_limit * 1024,
        'upload_limit_mb': settings.avatar_upload_limit / 1024.0,
        'allowed_extensions': avatars.uploaded.ALLOWED_EXTENSIONS,
        'allowed_mime_types': avatars.uploaded.ALLOWED_MIME_TYPES,
    })


@ajax_only
@deny_guests
@require_POST
@avatar_not_banned
def upload_avatar_handler(request):
    if not settings.allow_custom_avatars:
        raise AjaxError(_("Avatar uploads are currently disabled."))

    new_avatar = request.FILES.get('new-avatar');
    if not new_avatar:
        raise AjaxError(_("No file was sent."))

    try:
        avatars.uploaded.handle_uploaded_file(request.user, new_avatar)
    except ValidationError as e:
        raise AjaxError(e.args[0])

    return JsonResponse({'is_error': 0, 'message': 'Image has been uploaded.'})


@deny_guests
@avatar_not_banned
def crop_avatar(request, use_tmp_avatar):
    if use_tmp_avatar:
        if not avatars.uploaded.has_temporary_avatar(request.user):
            messages.error(request, _("Upload image that you want to crop."))
            return redirect('misago:usercp_change_avatar')
    else:
        if not avatars.uploaded.has_original_avatar(request.user):
            messages.error(request, _("You don't have uploaded image to crop."))
            return redirect('misago:usercp_change_avatar')

    if use_tmp_avatar:
        token = avatars.uploaded.avatar_source_token(request.user, 'tmp')
        avatar_url = reverse('misago:user_avatar_tmp', kwargs={
            'user_id': request.user.pk, 'token': token
        })
    else:
        token = avatars.uploaded.avatar_source_token(request.user, 'org')
        avatar_url = reverse('misago:user_avatar_org', kwargs={
            'user_id': request.user.pk, 'token': token
        })

    if request.method == 'POST':
        crop = request.POST.get('crop')
        try:
            if use_tmp_avatar:
                avatars.uploaded.crop_source_image(request.user, 'tmp', crop)
            else:
                avatars.uploaded.crop_source_image(request.user, 'org', crop)

            request.user.avatar_crop = crop
            request.user.save(update_fields=['avatar_crop'])

            if use_tmp_avatar:
                messages.success(request, _("Uploaded avatar was set."))
            else:
                messages.success(request, _("Avatar was cropped."))
            return redirect('misago:usercp_change_avatar')
        except ValidationError as e:
            messages.error(request, e.args[0])

    if not use_tmp_avatar and request.user.avatar_crop:
        user_crop = request.user.avatar_crop.split(',')
        current_crop = {
            'image_width': user_crop[0],
            'selection_len': user_crop[3],
            'start_x': user_crop[4],
            'start_y': user_crop[6],
        }
    else:
        current_crop = None

    return render(request, 'misago/usercp/crop_avatar.html', {
        'avatar_url': avatar_url,
        'crop': current_crop
    })


@deny_guests
@avatar_not_banned
def avatar_galleries(request):
    if not avatars.gallery.galleries_exist():
        messages.info(request, _("No avatars galleries exist."))
        return redirect('misago:usercp_change_avatar')

    if request.method == 'POST':
        new_image = request.POST.get('new-image')
        if new_image:
            if avatars.gallery.is_avatar_from_gallery(new_image):
                avatars.gallery.set_avatar(request.user, new_image)
                messages.success(request, _("Avatar from gallery was set."))
                return redirect('misago:usercp_change_avatar')
            else:
                messages.error(request, _("Incorrect image."))

    return render(request, 'misago/usercp/avatar_galleries.html', {
        'galleries': avatars.gallery.get_available_galleries()
    })


@deny_guests
def edit_signature(request):
    if not request.user.acl['can_have_signature']:
        raise Http404()

    form = EditSignatureForm(instance=request.user)
    if not request.user.is_signature_banned and request.method == 'POST':
        form = EditSignatureForm(request.POST, instance=request.user)
        if form.is_valid():
            set_user_signature(request.user, form.cleaned_data['signature'])
            request.user.save(update_fields=['signature', 'signature_parsed',
                                             'signature_checksum'])

            if form.cleaned_data['signature']:
                messages.success(request, _("Your signature has been edited."))
            else:
                message = _("Your signature has been cleared.")
                messages.success(request, message)
            return redirect('misago:usercp_edit_signature')

    acl = request.user.acl
    editor = Editor(form['signature'],
                    allow_blocks=acl['allow_signature_blocks'],
                    allow_links=acl['allow_signature_links'],
                    allow_images=acl['allow_signature_images'])
    return render(request, 'misago/usercp/edit_signature.html',
                  {'form': form, 'editor': editor})


@deny_guests
@transaction.atomic()
def change_username(request):
    namechanges = UsernameChanges(request.user)

    form = ChangeUsernameForm()
    if request.method == 'POST' and namechanges.left:
        form = ChangeUsernameForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                form.change_username(changed_by=request.user)

                message = _("Your username has been changed.")
                messages.success(request, message)

                return redirect('misago:usercp_change_username')
            except IntegrityError:
                message = _("Error changing username. Please try again.")
                messages.error(request, message)

    return render(request, 'misago/usercp/change_username.html', {
            'form': form,
            'changes_left': namechanges.left,
            'next_change_on': namechanges.next_on
        })


@sensitive_post_parameters()
@deny_guests
def change_email_password(request):
    form = ChangeEmailPasswordForm()
    if request.method == 'POST':
        form = ChangeEmailPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = ''
            new_password = ''

            # Store original data
            old_email = request.user.email
            old_password = request.user.password

            # Assign new creds to user temporarily
            if form.cleaned_data['new_email']:
                request.user.set_email(form.cleaned_data['new_email'])
                new_email = request.user.email
            if form.cleaned_data['new_password']:
                request.user.set_password(form.cleaned_data['new_password'])
                new_password = request.user.password

            request.user.email = old_email
            request.user.password = old_password

            credentials_token = cache_new_credentials(
                request.user, new_email, new_password)

            mail_subject = _("Confirm changes to %(username)s account "
                             "on %(forum_title)s forums")
            subject_formats = {'username': request.user.username,
                               'forum_title': settings.forum_name}
            mail_subject = mail_subject % subject_formats

            if new_email:
                # finally override email before sending message
                request.user.email = new_email

            mail_user(request, request.user, mail_subject,
                      'misago/emails/change_email_password',
                      {'credentials_token': credentials_token})

            message = _("E-mail was sent to %(email)s with a link that "
                        "you have to click to confirm changes.")
            messages.info(request, message % {'email': request.user.email})
            return redirect('misago:usercp_change_email_password')

    return render(request, 'misago/usercp/change_email_password.html',
                  {'form': form})


@deny_guests
def confirm_email_password_change(request, token):
    new_credentials = get_new_credentials(request.user, token)
    if not new_credentials:
        messages.error(request, _("Confirmation link is invalid."))
    else:
        changes_made = []
        if new_credentials['email']:
            request.user.set_email(new_credentials['email'])
            changes_made.extend(['email', 'email_hash'])
        if new_credentials['password']:
            request.user.password = new_credentials['password']
            update_session_auth_hash(request, request.user)
            changes_made.append('password')

        try:
            request.user.save(update_fields=changes_made)
            message = _("Changes in e-mail and password have been saved.")
            messages.success(request, message)
        except IntegrityError:
            messages.error(request, _("Confirmation link is invalid."))
    return redirect('misago:usercp_change_email_password')
