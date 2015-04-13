from django.contrib import auth
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from misago.users.decorators import deny_authenticated, deny_banned_ips
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
        return Response(form.get_errors_dict(),
                        status=status.HTTP_400_BAD_REQUEST)
