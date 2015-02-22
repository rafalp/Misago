from django.conf import settings
from django.contrib import auth
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
from misago.users.serializers import AuthenticatedUserSerializer


@sensitive_post_parameters()
@api_view(['POST'])
@never_cache
@deny_authenticated
@csrf_protect
@deny_banned_ips
def login(request):
    form = AuthenticationForm(request, data=request.data)
    if form.is_valid():
        auth.login(request, form.user_cache)
        return Response(AuthenticatedUserSerializer(form.user_cache).data)
    else:
        error = form.errors.as_data()['__all__'][0]
        return Response({
            'detail': error.messages[0],
            'code': error.code
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user(request):
    if request.user.is_authenticated():
        return Response(AuthenticatedUserSerializer(request.user).data)
    else:
        return Response({'id': None})

