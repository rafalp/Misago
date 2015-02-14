from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from misago.users.decorators import (deny_authenticated, deny_guests,
                                     deny_banned_ips)
from misago.users.forms.auth import AuthenticationForm


@sensitive_post_parameters()
@api_view(['POST'])
@never_cache
@deny_authenticated
@csrf_protect
@deny_banned_ips
def authenticate(request):
    form = AuthenticationForm(request, data=request.data)
    if form.is_valid():
        return Response()
    else:
        error = form.errors.as_data()['__all__'][0]
        return Response({
            'detail': error.messages[0],
            'code': error.code
        }, status=status.HTTP_400_BAD_REQUEST)
