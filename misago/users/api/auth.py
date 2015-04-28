from django.contrib import auth
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from misago.users.forms.auth import AuthenticationForm
from misago.users.rest_permissions import UnbannedAnonOnly
from misago.users.serializers import AuthenticatedUserSerializer


@api_view(['POST'])
@permission_classes((UnbannedAnonOnly,))
@csrf_protect
def login(request):
    form = AuthenticationForm(request, data=request.data)
    if form.is_valid():
        auth.login(request, form.user_cache)
        return Response(AuthenticatedUserSerializer(form.user_cache).data)
    else:
        return Response(form.get_errors_dict(),
                        status=status.HTTP_400_BAD_REQUEST)
