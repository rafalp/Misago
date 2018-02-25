from rest_framework import viewsets
from rest_framework.response import Response

from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from misago.acl import add_acl
from misago.threads.serializers import AttachmentSerializer, NewAttachmentSerializer


IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')


class AttachmentViewSet(viewsets.ViewSet):
    def create(self, request):
        if not request.user.acl_cache['max_attachment_size']:
            raise PermissionDenied(_("You don't have permission to upload new files."))

        serializer = NewAttachmentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        attachment = serializer.save()
        add_acl(request.user, attachment)
        return Response(AttachmentSerializer(attachment, context={'user': request.user}).data)
