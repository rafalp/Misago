from django.contrib import messages
from django.shortcuts import redirect, render as django_render
from django.utils.translation import ugettext as _

from misago.users.decorators import deny_guests
from misago.users.forms.usercp import ChangeForumOptionsForm
from misago.users.sites import usercp


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
def change_username(request):
    return render(request, 'misago/usercp/change_username.html')


@deny_guests
def change_email_password(request):
    return render(request, 'misago/usercp/change_email_password.html')
