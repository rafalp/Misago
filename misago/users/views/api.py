from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.core.decorators import ajax_only, require_POST

from misago.users import validators


def api(f):
    @sensitive_post_parameters
    @ajax_only
    @require_POST
    def decorator(request, *args, **kwargs):
        try:
            return JsonResponse({
                'has_error': 0,
                'message': f(request, *args, **kwargs),
            })
        except ValidationError as e:
            return JsonResponse({
                'has_error': 1,
                'message': unicode(e.message)
            })
    return decorator


@api
def validate_username(request, exclude=None):
    try:
        validators.validate_username(request.POST['username'])
        return _("Entered username is valid.")
    except KeyError:
        raise ValidationError(_('Enter username.'))


@api
def validate_email(request, exclude=None):
    try:
        validators.validate_email(request.POST['email'])
        return _("Entered e-mail is valid.")
    except KeyError:
        raise ValidationError(_('Enter e-mail address.'))


@api
def validate_password(request, exclude=None):
    try:
        validators.validate_password(request.POST['password'])
        return _("Entered password is valid.")
    except KeyError:
        raise ValidationError(_('Enter password.'))
