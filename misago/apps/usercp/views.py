from django.core.urlresolvers import NoReverseMatch
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.errors import error404
from misago.apps.profiles.decorators import user_view
from misago.decorators import block_guest, check_csrf
from misago.messages import Message
from misago.models import User
from misago.utils.translation import ugettext_lazy

def fallback(request):
    try:
        return redirect(request.POST.get('fallback', '/'))
    except NoReverseMatch:
        return redirect('index')


@block_guest
@check_csrf
@user_view
def follow(request, user):
    if request.user.pk == user.pk:
        return error404(request)
    if not request.user.is_following(user):
        request.messages.set_flash(Message(_("You are now following %(username)s") % {'username': user.username}), 'success')
        request.user.follows.add(user)
        request.user.following += 1
        request.user.save(force_update=True)
        user.followers += 1
        if not user.is_ignoring(request.user):
            alert = user.alert(ugettext_lazy("%(username)s is now following you").message)
            alert.profile('username', request.user)
            alert.save_all()
        else:
            user.save(force_update=True)
    return fallback(request)


@block_guest
@check_csrf
@user_view
def unfollow(request, user):
    if request.user.pk == user.pk:
        return error404(request)
    if request.user.is_following(user):
        request.messages.set_flash(Message(_("You have stopped following %(username)s") % {'username': user.username}))
        request.user.follows.remove(user)
        request.user.following -= 1
        request.user.save(force_update=True)
        user.followers -= 1
        user.save(force_update=True)
    return fallback(request)


@block_guest
@check_csrf
@user_view
def ignore(request, user):
    if request.user.pk == user.pk:
        return error404(request)
    if not request.user.is_ignoring(user):
        request.messages.set_flash(Message(_("You are now ignoring %(username)s") % {'username': user.username}), 'success')
        request.user.ignores.add(user)
    return fallback(request)


@block_guest
@check_csrf
@user_view
def unignore(request, user):
    if request.user.pk == user.pk:
        return error404(request)
    if request.user.is_ignoring(user):
        request.messages.set_flash(Message(_("You have stopped ignoring %(username)s") % {'username': user.username}))
        request.user.ignores.remove(user)
    return fallback(request)
