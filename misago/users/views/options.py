from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from misago.core.views import noscript

from misago.users.decorators import deflect_guests


@deflect_guests
def index(request):
    return redirect('options_form', form='forum-options')


@deflect_guests
def form(request):
    return noscript(request, **{
        'title': _("Options"),
        'message': _("To change options enable JS."),
    })


# DEPRECATED VIEWS - DELETE AFTER USER CP IS DONE
def edit_signature(request):
    if not request.user.acl['can_have_signature']:
        raise Http404()

    if request.method == "GET":
        read_user_notifications(request.user,
                                'usercp_signature_%s' % request.user.pk)

    form = EditSignatureForm(instance=request.user)
    if not request.user.is_signature_locked and request.method == 'POST':
        form = EditSignatureForm(request.POST, instance=request.user)
        if form.is_valid():
            set_user_signature(
                request, request.user, form.cleaned_data['signature'])
            request.user.save(update_fields=[
                'signature', 'signature_parsed', 'signature_checksum'
            ])

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

            mail_subject = _("Confirm changes to %(user)s account "
                             "on %(forum_title)s forums")
            subject_formats = {'user': request.user.username,
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
