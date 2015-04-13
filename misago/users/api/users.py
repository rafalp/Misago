from django.contrib.auth import get_user_model

from rest_framework import status, viewsets
from rest_framework.response import Response

from misago.users.forms.register import RegisterForm


class UserViewSet(viewsets.ViewSet):
    """
    API endpoint for users manipulation
    """
    queryset = get_user_model().objects.all()

    def list(self, request):
        pass

    def create(self, request):
        """
        POST to /api/users is treated as new user registration
        """
        form = RegisterForm(request.data)
        if form.is_valid():
            return Response({'detail': 'Wolololo!'})
        else:
            return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)
