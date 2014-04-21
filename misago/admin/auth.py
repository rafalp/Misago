from hashlib import md5
from django.contrib import auth as dj_auth


def make_user_admin_token(user):
    formula = '%s:%s:%s' % (user.pk, user.email, user.password)
    return md5(formula).hexdigest()


def login(request, user):
    request.session['misago_admin_token'] = make_user_admin_token(user)
    dj_auth.login(request, user)


def logout(request):
    pass


def is_admin_session(request):
    if request.user.is_anonymous():
        return False

    if not (request.user.is_staff and request.user.is_superuser):
        return False

    admin_token = request.session.get('misago_admin_token')
    return admin_token == make_user_admin_token(request.user)
